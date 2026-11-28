"""Retrieval evaluation on this repository's documents (SPEC-0212 TSK-0119).

The experiment criterion 70 deferred, run on data the owner holds: every
Markdown document under docs/ at one commit. Each document's frontmatter
title is a query whose answer is that document; the title heading and the
lines most documents share (template boilerplate) are removed from the
indexed text so a query cannot match its own title verbatim. Documents are
ordered by the commit that first added them: the earlier share tunes the
hybrid fusion constant, the later share reports the result.

``build`` runs on the host (it needs git) and writes the corpus as JSONL.
``run`` runs beside Ollama, Qdrant and MLflow on ai_net: it embeds chunks with
the local embedding model, indexes them in a throwaway Qdrant collection,
scores BM25, dense and reciprocal-rank-fusion retrieval, logs to MLflow and
deletes the collection. The Qdrant key is read from a file and never printed.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
from collections import Counter
from collections.abc import Iterable, Sequence
from pathlib import Path

TOKEN = re.compile(r"[0-9a-z가-힣]+")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
TITLE = re.compile(r'^title:\s*"?(.*?)"?\s*$', re.M)
BOILERPLATE_SHARE = 0.2
TUNE_SHARE = 0.8
RRF_KS = (10, 30, 60)
KS = (1, 5, 10)


def tokenize(text: str) -> list[str]:
    return TOKEN.findall(text.lower())


def parse_document(raw: str) -> tuple[str, str] | None:
    """(title, body) without frontmatter or the title heading; None without a title."""
    match = FRONTMATTER.match(raw)
    if not match:
        return None
    title = TITLE.search(match.group(1))
    if not title or not title.group(1).strip():
        return None
    name = title.group(1).strip()
    body = [
        line
        for line in raw[match.end() :].splitlines()
        if line.strip().lstrip("#").strip() != name
    ]
    return name, "\n".join(body)


def strip_boilerplate(
    bodies: Sequence[str], share: float = BOILERPLATE_SHARE
) -> list[str]:
    """Drop non-blank lines that occur in at least ``share`` of the documents."""
    seen = Counter(
        line
        for body in bodies
        for line in {x.strip() for x in body.splitlines()}
        if line
    )
    limit = max(2, math.ceil(share * len(bodies)))
    common = {line for line, count in seen.items() if count >= limit}
    return [
        "\n".join(x for x in body.splitlines() if x.strip() not in common)
        for body in bodies
    ]


def time_split(docs: Sequence[dict], share: float = TUNE_SHARE) -> tuple[list, list]:
    ordered = sorted(docs, key=lambda d: (d["created"], d["path"]))
    cut = int(len(ordered) * share)
    return ordered[:cut], ordered[cut:]


class BM25:
    def __init__(self, docs: Sequence[Sequence[str]], k1: float = 1.2, b: float = 0.75):
        self.docs = [Counter(d) for d in docs]
        self.lengths = [len(d) for d in docs]
        self.avg = sum(self.lengths) / max(1, len(docs))
        df = Counter(t for d in self.docs for t in d)
        n = len(docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}
        self.k1, self.b = k1, b

    def rank(self, query: Sequence[str], limit: int = 50) -> list[int]:
        scores = []
        for i, counts in enumerate(self.docs):
            norm = self.k1 * (1 - self.b + self.b * self.lengths[i] / (self.avg or 1))
            s = sum(
                self.idf[t] * counts[t] * (self.k1 + 1) / (counts[t] + norm)
                for t in set(query)
                if counts.get(t)
            )
            if s > 0:
                scores.append((s, i))
        scores.sort(key=lambda x: (-x[0], x[1]))
        return [i for _, i in scores[:limit]]


def rrf(rankings: Iterable[Sequence[int]], k: int) -> list[int]:
    score: dict[int, float] = {}
    for ranking in rankings:
        for pos, doc in enumerate(ranking):
            score[doc] = score.get(doc, 0.0) + 1.0 / (k + pos + 1)
    return sorted(score, key=lambda d: (-score[d], d))


def metrics(results: Sequence[tuple[int, Sequence[int]]]) -> dict[str, float]:
    """Recall@k and MRR@10 over (answer, ranking) pairs."""
    n = max(1, len(results))
    out = {f"recall_at_{k}": sum(a in r[:k] for a, r in results) / n for k in KS}
    out["mrr_at_10"] = (
        sum(1 / (list(r).index(a) + 1) for a, r in results if a in r[:10]) / n
    )
    out["queries"] = float(len(results))
    return out


# Ollama embeds text as is; these model families expect their own query and
# document prompts (https://qdrant.tech/documentation/embeddings/ollama/).
PROMPTS = {
    "embeddinggemma": ("task: search result | query: ", "title: none | text: "),
    "qwen3-embedding": (
        "Instruct: Given a web search query, retrieve relevant passages that "
        "answer the query\nQuery:",
        "",
    ),
    "nomic-embed-text": ("search_query: ", "search_document: "),
}


def prompted(model: str, texts: list[str], query: bool) -> list[str]:
    """Prefix texts with the model family's query or document prompt."""
    for family, pair in PROMPTS.items():
        if model.startswith(family):
            return [pair[0 if query else 1] + t for t in texts]
    return texts


def chunks(text: str, size: int = 1200, limit: int = 6) -> list[str]:
    out: list[str] = []
    cur: list[str] = []
    length = 0
    for word in text.split():
        cur.append(word)
        length += len(word) + 1
        if length >= size:
            out.append(" ".join(cur))
            cur, length = [], 0
            if len(out) == limit:
                return out
    if cur:
        out.append(" ".join(cur))
    return out or [""]


# --- host step -------------------------------------------------------------


def _git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args], check=True, capture_output=True, text=True
    ).stdout


def assemble(raw_docs: Sequence[tuple[str, str, str]]) -> list[dict]:
    """Corpus rows from (path, created, raw) triples; ambiguous titles are dropped."""
    parsed = []
    for path, created, raw in raw_docs:
        doc = parse_document(raw)
        if doc:
            parsed.append(
                {"path": path, "title": doc[0], "created": created, "body": doc[1]}
            )
    titles = Counter(d["title"] for d in parsed)
    parsed = [d for d in parsed if titles[d["title"]] == 1]
    texts = strip_boilerplate([d.pop("body") for d in parsed])
    for d, text in zip(parsed, texts, strict=True):
        d["text"] = text
    return parsed


def build(root: Path, commit: str) -> list[dict]:
    listing = _git(root, "ls-tree", "-r", "--name-only", commit, "docs")
    paths = [p for p in listing.splitlines() if p.endswith(".md")]
    created: dict[str, str] = {}
    when = ""
    log = _git(
        root,
        "log",
        "--no-renames",
        "--diff-filter=A",
        "--format=@%cI",
        "--name-only",
        commit,
        "--",
        "docs",
    )
    for line in log.splitlines():
        if line.startswith("@"):
            when = line[1:]
        elif line:
            # newest first: the last write is the first add (a move counts as an add)
            created[line] = when
    return assemble(
        [
            (p, created[p], _git(root, "show", f"{commit}:{p}"))
            for p in paths
            if p in created
        ]
    )


# --- container step --------------------------------------------------------


def _http(method: str, url: str, body=None, headers=None, timeout: int = 600):
    import requests

    response = requests.request(
        method, url, json=body, headers=headers or {}, timeout=timeout
    )
    response.raise_for_status()
    return response.json() if response.content else {}


def run(args) -> dict:
    import mlflow

    docs = [json.loads(x) for x in Path(args.corpus).read_text().splitlines()]
    tune, test = time_split(docs)
    index = {d["path"]: i for i, d in enumerate(docs)}
    bm25 = BM25([tokenize(d["text"]) for d in docs])
    auth = {"api-key": Path(args.qdrant_key_file).read_text().strip()}
    coll = f"docs_eval_{args.commit[:12]}"

    def embed(texts: list[str], query: bool) -> list[list[float]]:
        # truncate=False: an over-long input fails instead of embedding a prefix.
        body = {
            "model": args.model,
            "input": prompted(args.model, texts, query),
            "truncate": False,
        }
        return _http("POST", f"{args.ollama}/api/embed", body)["embeddings"]

    pieces = [(i, c) for i, d in enumerate(docs) for c in chunks(d["text"])]
    vectors: list[list[float]] = []
    for s in range(0, len(pieces), 32):
        vectors += embed([c for _, c in pieces[s : s + 32]], False)
    qvec = embed([d["title"] for d in docs], True)
    base = f"{args.qdrant}/collections/{coll}"
    _http(
        "PUT", base, {"vectors": {"size": len(vectors[0]), "distance": "Cosine"}}, auth
    )
    try:
        for s in range(0, len(pieces), 256):
            points = [
                {"id": j, "vector": vectors[j], "payload": {"doc": pieces[j][0]}}
                for j in range(s, min(s + 256, len(pieces)))
            ]
            _http("PUT", f"{base}/points?wait=true", {"points": points}, auth)

        def dense(i: int) -> list[int]:
            body = {"vector": qvec[i], "limit": 60, "with_payload": True}
            hits = _http("POST", f"{base}/points/search", body, auth)["result"]
            seen: list[int] = []
            for hit in hits:
                if hit["payload"]["doc"] not in seen:
                    seen.append(hit["payload"]["doc"])
            return seen[:50]

        ranks = {
            d["path"]: (bm25.rank(tokenize(d["title"])), dense(index[d["path"]]))
            for d in docs
        }
    finally:
        if not args.keep_collection:
            _http("DELETE", base, headers=auth)

    def score(split, method: str, k: int = 60) -> dict[str, float]:
        pairs = []
        for d in split:
            lexical, vector = ranks[d["path"]]
            ranking = {"bm25": lexical, "dense": vector}.get(method) or rrf(
                [lexical, vector], k
            )
            pairs.append((index[d["path"]], ranking))
        return metrics(pairs)

    best_k = max(RRF_KS, key=lambda k: score(tune, "hybrid", k)["mrr_at_10"])
    result: dict = {"best_rrf_k": best_k}
    for name, split in (("tune", tune), ("test", test)):
        result[name] = {m: score(split, m, best_k) for m in ("bm25", "dense", "hybrid")}
    mlflow.set_tracking_uri(args.mlflow)
    mlflow.set_experiment("docs-retrieval-eval")
    with mlflow.start_run(run_name=f"docs@{args.commit[:12]}") as active:
        mlflow.log_params(
            {
                "commit": args.commit,
                "model": args.model,
                "docs": len(docs),
                "chunks": len(pieces),
                "tune_docs": len(tune),
                "test_docs": len(test),
                "cutoff": test[0]["created"] if test else "",
                "best_rrf_k": best_k,
                "boilerplate_share": BOILERPLATE_SHARE,
            }
        )
        for name in ("tune", "test"):
            for method, values in result[name].items():
                mlflow.log_metrics(
                    {f"{name}_{method}_{k}": v for k, v in values.items()}
                )
        mlflow.log_dict(result, "result.json")
        result["mlflow_run_id"] = active.info.run_id
    return result


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="write the corpus JSONL from git (host)")
    b.add_argument("--commit", required=True)
    b.add_argument("--out", required=True)
    r = sub.add_parser("run", help="embed, index, score and log (container on ai_net)")
    r.add_argument("--corpus", required=True)
    r.add_argument("--commit", required=True)
    r.add_argument("--qdrant-key-file", required=True)
    r.add_argument("--qdrant", default="http://qdrant:6333")
    r.add_argument("--ollama", default="http://ollama:11434")
    r.add_argument("--mlflow", default="http://mlflow:5000")
    r.add_argument("--model", default="embeddinggemma-2:740m")
    r.add_argument("--keep-collection", action="store_true")
    args = parser.parse_args(argv)
    if args.cmd == "build":
        docs = build(Path(__file__).resolve().parents[3], args.commit)
        Path(args.out).write_text(
            "".join(json.dumps(d, ensure_ascii=False) + "\n" for d in docs)
        )
        print(f"docs={len(docs)}")
    else:
        print(json.dumps(run(args), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

---
title: "BLOCKED: secret content read"
version: "2.0.0"
type: "governance/rule"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: 'BLOCKED: secret content read'
  layer: agent
updated: "2026-11-20"
action: "block"
enabled: true
event: "bash"
name: "block-secret-content-read"
pattern: "(?:(?:^|[\\n;&|(`{]|\\$\\()\\s*(?:(?:[A-Za-z_]\\w*=\\S*|env|command|exec|time|nice|then|do|else|!|\\{|timeout\\s+\\S+|sudo)\\s+)*(?:cat|tac|head|tail|less|more|bat|grep|egrep|fgrep|rg|sed|awk|cut|sort|uniq|nl|xxd|od|hexdump|strings|base64|diff|cmp|jq|yq|source|paste|rev|fold|vi|vim|view|nano)\\b(?:'[^'\\n]*'|\\\"[^\\\"\\n]*\\\"|[^;&|\\n'\\\"])*?(?<=[\\s/])(?:secrets(?:/[^\\s;&|'\\\"<>(){}]*)?|[\\w-]*\\.env(?:\\.(?!example\\b)[\\w.-]+)?)(?=[\\s;&|)}]|$))|(?:<\\s*(?:[^\\s;&|'\\\"<>()]*/)?(?:secrets(?:/[^\\s;&|'\\\"<>(){}]*)?|[\\w-]*\\.env(?:\\.(?!example\\b)[\\w.-]+)?)(?=[\\s;&|)}]|$))"
---

# BLOCKED: secret content read

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the rule payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Purpose

##### Objective

Apply the declared `block` action for block-secret-content-read.

##### Authority

[Environment constraints](../environment-constraints.md#22-approved-secrets-work-protocol),
ENVIRONMENT-CONSTRAINTS-R34 and R164: an agent never prints or quotes a
secret value, so a shell command does not read the content of a secret
file or an environment file.

#### Scope

##### Applies To

The declared `bash` event and `pattern` match a command whose reader
(`cat`, `head`, `tail`, `less`, `grep`, `rg`, `sed`, `awk`, `cut`, `sort`,
`xxd`, `od`, `strings`, `base64`, `diff`, `jq`, `source`, `paste`, `vim`
and similar) names a `secrets` directory, a file under one, or a `.env`
file such as `.env`, `prod.env` or `.env.local` other than `.env.example`,
or that redirects such a file into a command with `<`. The reader may
follow a newline or another command separator, an environment assignment,
`env`, `command`, `exec`, `timeout`, `sudo`, `then`, `do` or `{`, and
quoted arguments before the path may contain `;` or `|`.

##### Exclusions

Metadata stays allowed: listing, finding, `stat`, `test` and `wc -c`, a
quoted search term such as `grep -rn '.env' docs`, `.env.example`, and a
program given the path as an option, such as `docker compose --env-file
.env` or `lab.py --env-file labs/.env`. An unquoted search word `secrets`
after a reader is refused; quote it.

#### Rules

##### Requirements

```bash
# BLOCKED: secret or environment file content
cat secrets/db/mng-pg/password.txt
grep -n KEY .env

# ALLOWED: metadata only
ls -la secrets/db
test -s secrets/db/password.txt
```

The declared action applies when the pattern matches.

##### Enforcement

The shared dispatcher evaluates the rule before a provider runs the command,
for both providers. It sees the command text only. Outside it: a quoted
path, a path built at run time or held in a variable, an interpreter or
script that reads the file (`python3`, `perl`), `find -exec`, `xargs`,
`git show` of a revision, a recursive read of a parent directory, a hook
bypass, and `docker compose config` without `--services`, which prints
interpolated values. On a provider with its own read deny, that deny still
applies.

#### Exceptions

##### Exception Conditions

The rule grants no bypass. An approved secret operation (R28 to R33) runs
through a registered script that never prints the value, or the user runs
the command.

##### Approval and Review

None.

#### Ownership

##### Responsibilities

`@buenhyden`.

##### Change and Adoption

Changes land with their Task evidence and the rule test
`tests/lib/hooks/test_secret_read_rule.py`.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.

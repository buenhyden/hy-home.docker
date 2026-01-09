---
trigger: always_on
glob: "**/*.py"
description: "NLTK: Text Processing, Corpora Management, and Tokenization specific rules."
---
# NLTK Specific Rules

## 1. Performance

- **Tokenizers**: Use `RegexpTokenizer` or `ToktokTokenizer` for large texts instead of default `word_tokenize` (which can be slow).
- **Lazy Loading**: Guard corpus downloads (`nltk.download`) to run only when needed/missing.

### Example: Performance Tokenization

#### Good (Implementation)

```python
tokenizer = RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(text)
```

## 2. Modular Processing

- **Pure Functions**: Encapsulate steps (tokenization, stopwords, stemming) in pure functions.
- **Explicit Objects**: Pass stemmers/lemmatizers as arguments rather than instantiating them repeatedly inside loops.

### Example: Modular Pipeline

#### Good (Implementation)

```python
def process_text(text: str, stemmer: PorterStemmer) -> List[str]:
    tokens = word_tokenize(text)
    return [stemmer.stem(t) for t in tokens]
```

## 3. Best Practices

- **POS Tagging**: Use POS tags when lemmatizing (`WordNetLemmatizer`). Without POS tags, lemmatization is often incorrect.
- **Type Hints**: Use `List[str]` for token lists.

### Example: Correct Lemmatization

#### Good (Implementation)

```python
# Convert NLTK tag to WordNet tag, then lemmatize
lemma = lemmatize(word, pos=get_wordnet_pos(tag))
```

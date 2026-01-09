---
trigger: always_on
glob: "**/*.py"
description: "LangChain: LCEL Chains, Agents, and Prompt Template Best Practices."
---
# LangChain Standards

## 1. LCEL (LangChain Expression Language)

- **Chaining**: Use the pipe operator (`|`) to compose chains: `prompt | llm | parser`.
- **Legacy Avoidance**: Do not use deprecated `LLMChain`, `SequentialChain`.

### Example: LCEL

**Good**

```python
from langchain_core.runnables import RunnablePassthrough
chain = prompt | llm | parser
result = chain.invoke({"input": "hello"})
```

**Bad**

```python
from langchain.chains import LLMChain # Deprecated
chain = LLMChain(llm=llm, prompt=prompt)
```

## 2. Agents (LangGraph)

- **Stateful Agents**: Use `LangGraph` for complex, multi-step agents with loops.
- **Tools**: Define tools using `@tool` decorator with clear docstrings for LLM to understand.

### Example: Tool

**Good**

```python
@tool
def search_database(query: str) -> str:
    """Search the product database."""
    return db.search(query)
```

**Bad**

```python
def search(q): # No decorator, no docstring
    return db.search(q)
```

## 3. Structured Output

- **Pydantic**: Use `.with_structured_output(MyModel)` for reliable JSON schema output.
- **Streaming**: For UX, design chains to support `.stream()` for real-time token display.

## 4. Secrets

- **No Hardcoding**: Use `os.environ["OPENAI_API_KEY"]` or `.env` files.

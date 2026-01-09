---
trigger: always_on
glob: "**/*.{py,ts,tsx,js,jsx}"
description: "AI Engineering: Structured Output, Evals, and Prompts."
---
# AI Engineering Standards

## 1. Structured Output

- **JSON Mode**: Use Schema-enforced output (Pydantic/Zod objects). Never parse raw strings if possible.
- **Validation**: Retry on validation error.

### Example: Validated Output

**Good (LangChain)**

```python
parser = PydanticOutputParser(pydantic_object=Actor)
prompt = PromptTemplate(..., partial_variables={"format_instructions": parser.get_format_instructions()})
```

**Bad**

```python
# "Please output JSON" in prompt manualy
response = json.loads(llm_response) # Might fail randomly
```

## 2. Prompt Engineering

- **Separation**: System Prompt (Instruction) vs User Prompt (Data).
- **Delimiters**: Use XML tags `<context>` to separate instructions from data.

### Example: Delimiters

**Good**

```text
Analyze constraints in <constraints>...</constraints>
and apply to <data>...</data>
```

**Bad**

```text
Analyze constraints ... and apply to ... 
(LLM confuses instructions with data injection)
```

## 3. Evals

- **Unit Tests**: Test prompts against golden examples.
- **Asserts**: "Refusal" checks ("I cannot help") should fail the test.

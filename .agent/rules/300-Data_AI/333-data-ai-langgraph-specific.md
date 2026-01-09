---
trigger: always_on
glob: "**/*.py"
description: "LangGraph: Agent Workflows, State Management, and Graph Topology."
---
# LangGraph Standards

## 1. Graph Topology & Modularity

- **Single Responsibility**: Each node should have ONE clear purpose.
- **Subgraphs**: Encapsulate common patterns into reusable subgraphs.
- **DAGs**: Prefer Directed Acyclic Graphs. Use cycles only for feedback loops.

### Example: Subgraph

**Good**

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

class AgentState(TypedDict):
    messages: List[str]
    tool_output: str | None

def fetch_data_node(state: AgentState) -> AgentState:
    return {"messages": state["messages"] + ["Data fetched."]}

def build_subgraph():
    builder = StateGraph(AgentState)
    builder.add_node("fetch", fetch_data_node)
    builder.set_entry_point("fetch")
    builder.set_finish_point("fetch")
    return builder.compile()
```

**Bad**

```python
# Massive monolithic graph with 50+ nodes in a single function
# No reusable subgraphs, impossible to test
```

## 2. State Management

- **TypedDict**: Define state schema with `TypedDict` for type safety.
- **Immutability**: Return NEW state dicts from nodes, don't mutate.
- **Checkpointing**: Enable checkpoints for durable execution.

## 3. Integration with LangChain

- **LCEL**: Use LangChain Expression Language (`|`) for chains within nodes.
- **create_agent**: Use `create_agent()` for ReAct pattern agents.

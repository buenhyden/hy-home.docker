---
trigger: always_on
glob: "**/*.md,**/*.mmd"
description: "Mermaid: Diagram Types, Syntax, Validation, and Best Practices."
---
# Mermaid Standards

## 1. Diagram Types

- **Flowchart**: Process and logic flow (`flowchart TD`).
- **Sequence**: Interaction flows between actors.
- **ERD**: Database schemas and data models.
- **Class**: Object-oriented design.

### Example: Flowchart

**Good**

```mermaid
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process]
    B -->|No| D[End]
```

### Example: Sequence

**Good**

```mermaid
sequenceDiagram
    Client->>Server: Request
    Server->>Database: Query
    Database-->>Server: Result
    Server-->>Client: Response
```

## 2. Syntax Best Practices

- **Quote Labels**: Use `id["Label (with parens)"]` for special characters.
- **No HTML**: Avoid HTML tags in labels.
- **Subgraphs**: Group related nodes for organization.

### Example: ERD

**Good**

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
```

## 3. Validation

- **Compile Check**: Run `npx @mermaid-js/mermaid-cli mmdc -i input.md -o output.svg`.
- **Preview**: Use VS Code Mermaid Preview extension.

## 4. Documentation Use

- **Architecture**: Use flowcharts for system architecture.
- **API Flows**: Use sequence diagrams for API documentation.
- **Data Models**: Use ERDs for database documentation.

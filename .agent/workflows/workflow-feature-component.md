---
description: Standard workflow for implementing features or components
---

# Feature/Component Implementation Workflow

Based on `098-core-create-command-specific.md`, `102-frontend-project-structure-specific.md`, and `202-backend-project-structure-specific.md`.

1. **Analysis**
   - Understand requirements.
   - Identify domain/feature area.

2. **Structure Creation**
   - Create directory structure if needed (Feature-first).
   - Frontend: `src/features/<feature>/`
   - Backend: `src/<domain>/`

3. **Scaffolding**
   - Create base files (Controller/Service or Component/Hook).
   - Add types/DTOs.

4. **Implementation**
   - Implement core logic.
   - Follow strict typing rules.

5. **Testing**
   - Add unit tests co-located or in `tests/`.

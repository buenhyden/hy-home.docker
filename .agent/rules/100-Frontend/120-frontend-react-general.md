---
trigger: always_on
glob: "**/*.{jsx,tsx}"
description: "React: Hooks usage, Functional Components, and Keys."
---
# React General Standards

## 1. Components & Props

- **Functional**: Always use Functional Components. No Class Components.
- **Props**: Destructure props directly in signature.

### Example: Component

**Good**

```tsx
const UserCard = ({ name, email }: UserProps) => (
  <div>{name}</div>
);
```

**Bad**

```tsx
class UserCard extends React.Component { ... }
```

## 2. Hooks Rules

- **Top Level**: Never call hooks inside loops/conditions.
- **Dependencies**: `useEffect` dependency array must be exhaustive.

### Example: useEffect

**Good**

```tsx
useEffect(() => {
  fetchData(id);
}, [id]); // id is a dependency
```

**Bad**

```tsx
useEffect(() => {
  fetchData(id);
}, []); // Bug: id changes won't re-fetch
```

## 3. Keys & Lists

- **Stable Keys**: Use unique IDs from data. NEVER use index as key for mutable lists.

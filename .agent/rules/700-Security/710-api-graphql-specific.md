---
trigger: always_on
glob: "**/*.graphql"
description: "GraphQL: Schema design, N+1 prevention, Security, and Introspection."
---
# GraphQL Standards

## 1. Schema Design

- **Nullability**: Fields should be non-nullable (`!`) by default unless optional.
- **Relay Spec**: Implement Relay Connection spec (`edges`, `node`, `cursor`) for collections.

### Example: Nullability

**Good**

```graphql
type User {
  id: ID!
  username: String!
  email: String # Optional
}
```

**Bad**

```graphql
type User {
  id: ID # Why would ID be null?
}
```

## 2. Operations & Performance

- **Depth Limit**: Enforce query depth checks to prevent DoS.
- **Batching**: Use DataLoader to solve N+1 on resolvers.

### Example: N+1

**Good (DataLoader)**

```js
return userLoader.load(authorId); // Batches IDs
```

**Bad**

```js
return db.getUser(authorId); // 1 SQL per Post
```

## 3. Security

- **Introspection**: DISABLE introspection in production (`introspection: false`).
- **Persisted Queries**: Use persisted queries (allowlist) to prevent arbitrary query injection.

### Example: Introspection

**Good (Production)**

```ts
new ApolloServer({ introspection: false, playground: false });
```

**Bad**

```ts
new ApolloServer({ introspection: true }); // Exposes schema to attackers
```

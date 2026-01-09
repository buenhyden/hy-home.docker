---
trigger: always_on
glob: "**/*.js,**/*.ts"
description: "MongoDB: Scalable NoSQL document database best practices."
---
# MongoDB Standards

## 1. Schema Design (Modeling)

- **Embedding vs. Referencing**: Embed data that is always read together. Reference data that grows unboundedly or is shared across many documents.
- **Size Limit**: Stay well below the 16MB BSON document limit.
- **Flexibility**: Use the `Attribute Pattern` for polymorphic schemas.

## 2. Indexing

- **Multikey Indexes**: Use for arrays.
- **TTL Indexes**: Use for expiring data (e.g., sessions, logs).
- **Compound Indexes**: Order matters (Equality, Sort, Range).

## 3. Aggregation Framework

- **Pipeline**: Use `$match` and `$project` early in the pipeline to reduce data volume.
- **Optimization**: Ensure the first stage of the pipeline uses an index if possible.

## 4. Connectivity & Drivers

- **Mongoose**: Define strict schemas with validation. Use `.lean()` for read-only queries to improve performance.
- **Write Concern**: Use `w: "majority"` for critical data.

## 5. Security

- **RBAC**: Enable authentication and use built-in roles.
- **Network**: Isolate MongoDB in a private VPC.

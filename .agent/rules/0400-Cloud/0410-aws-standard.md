---
trigger: model_decision
glob: ["**/*.tf", "**/*.yml", "**/*.json"]
description: "AWS Cloud Standards: Best practices for Lambda, Serverless, and Advanced Architecture."
---

# 0410-Cloud-AWS

- **Role**: Cloud Architect / DevOps
- **Purpose**: Specific standards for AWS services (Lambda, DynamoDB, S3, API Gateway).
- **Activates When**: Working with AWS resources or Serverless Application Model (SAM).

## 1. Standards

### 1.1 Principles

- **[REQ-AWS-GEN-01] Serverless First**: Prefer Lambda/Fargate over EC2.
- **[REQ-AWS-GEN-02] Managed Services**: Use SQS/SNS/EventBridge over running RabbitMQ/Kafka on EC2.
- **[REQ-AWS-GEN-03] Security**: Service Control Policies (SCPs) MUST enforce guardrails.

### 1.2 Scope

- **In-Scope**: AWS Lambda, DynamoDB, S3, EventBridge.
- **Out-of-Scope**: General Cloud Principles (see 0400).

### 1.3 Must / Must Not

- **[REQ-AWS-LMB-01] Runtime**: Lambda MUST use supported runtimes (Node.js 18+, Python 3.10+).
- **[REQ-AWS-IAM-01] Roles**: Each Lambda MUST have its own dedicated IAM Role (1:1).
- **[BAN-AWS-LMB-01] No Monoliths**: Lambda functions MUST be single-purpose (SRP).
- **[REQ-AWS-DDB-01] Single Table**: Advanced designs SHOULD consider Single Table Design (if access patterns are known).

## 2. Procedures

### 2.1 Lambda Cold Start Optimization

1. **Minify**: Bundle code with esbuild/webpack.
2. **Provisioned Concurrency**: Enable for latency-sensitive paths.
3. **Keep-Warm**: Avoid manual pingers; uses Provisioned Concurrency.

### 2.2 Event-Driven Architecture

1. **Source**: S3 Upload / API Call.
2. **Bus**: EventBridge (Schema Registry).
3. **Consumer**: Lambda / SQS.
4. **DLQ**: Dead Letter Queues on ALL asynchronous sources.

## 3. Examples

### 3.1 Lambda (SAM)

```yaml
Type: AWS::Serverless::Function
Properties:
  Handler: index.handler
  Runtime: nodejs18.x
  Policies:
    - DynamoDBCrudPolicy:
        TableName: !Ref MyTable
  Environment:
    Variables:
      TABLE_NAME: !Ref MyTable
```

## 4. Validation Criteria

- [ ] **[VAL-AWS-IAM-01]** No `*` Resource in IAM policies.
- [ ] **[VAL-AWS-BSL-01]** Public Access Block enabled on S3 buckets.
- [ ] **[VAL-AWS-LMB-01]** Lambda functions have X-Ray Tracing enabled.

## 5. References

- Related: [0320-infrastructure-terraform.md](../0300-DevOps_and_Infrastructure/0320-infrastructure-terraform.md)

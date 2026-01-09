---
trigger: always_on
glob: "**/*.{ts,js,py}"
description: "AWS CDK, Lambda, and Well-Architected best practices."
---
# AWS Standards

## 1. CDK v2

- **Mandatory**: Use CDK v2 exclusively.
- **Constructs**: Modularize into reusable Constructs.
- **Stacks**: Organize into logical stacks (`DataStack`, `ApiStack`).

## 2. Lambda

- **SDK Init**: Initialize clients outside handler (reuse execution environment).
- **Config**: Use environment variables or Parameter Store. No hardcoded secrets.
- **Idempotent**: Design idempotent functions. Use AWS Powertools.
- **Memory**: Tune memory based on CloudWatch metrics.

## 3. IAM

- **Least Privilege**: Grant only necessary permissions.
- **`cdk-nag`**: Enforce policies with `cdk-nag`.

## 4. Serverless Patterns

- **DLQ**: Use Dead-Letter Queues for Lambda failures.
- **Event-Driven**: Prefer EventBridge, SQS, SNS.
- **Avoid Recursion**: Never trigger Lambda recursively.

## 5. Testing

- **Unit**: CDK Assertions for constructs.
- **Integration**: Test deployed services.

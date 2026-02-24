# RabbitMQ Operational Blueprint

> **Component**: `rabbitmq`
> **Profile**: `rabbitmq` (Optional Tier)

## 1. Role in Ecosystem

RabbitMQ serves as the secondary AMQP broker, typically utilized for task-based async worker queues and legacy system integrations.

- **AMQP Port**: `5672`
- **Management Web UI**: `https://rabbitmq.${DEFAULT_URL}`

## 2. Configuration Standards

The deployment uses a declarative `rabbitmq.conf` file.

- **Erlang Cookie**: Managed via Docker Secret `rabbitmq_erlang_cookie`.
- **Definition Export**: Regularly export definitions from the Web UI to keep a record of exchanges and bindings.

## 3. Troubleshooting Persistence

If the service fails to boot with "Permission Denied", check the host volume permission on `${DEFAULT_DATA_DIR}/rabbitmq`. RabbitMQ demands UID `999`.

```bash
# Fix permissions on host
sudo chown -R 999:999 data/rabbitmq
```

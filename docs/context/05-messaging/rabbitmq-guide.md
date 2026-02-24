# RabbitMQ Operational Blueprint

> **Component**: `rabbitmq`
> **Profile**: `rabbitmq` (Optional Tier)

## 1. Role in Ecosystem

RabbitMQ serves as the secondary AMQP broker, typically utilized for task-based async worker queues and legacy system integrations.

- **AMQP Port**: `5672` (Internal)
- **Management Web UI**: `https://rabbitmq.${DEFAULT_URL}`

### Technical Specifications

| Attribute | Internal DNS | Port | Hardening |
| --- | --- | --- | --- |
| **Service** | `rabbitmq` | `5672` | Standard (`no-new-privileges`) |
| **Management**| `rabbitmq` | `15672` | [Hardened] |
| **Secrets** | `rabbitmq_user` | `rabbitmq_password` | [Docker Secrets] |

## 2. Initial Setup

The deployment is declarative via `rabbitmq.conf`.

- **Erlang Cookie**: Managed via Docker Secret `rabbitmq_erlang_cookie`.
- **Initialization**: Upon first boot, enable required plugins (e.g., `rabbitmq_management`) if not defined in the base image.

## 3. Configuration Standards

- **Definition Export**: Regularly export definitions from the Web UI to keep a record of exchanges and bindings.

## 4. Troubleshooting Persistence

If the service fails to boot with "Permission Denied", check the host volume permission on `${DEFAULT_DATA_DIR}/rabbitmq`. RabbitMQ demands UID `999`.

```bash
# Fix permissions on host
sudo chown -R 999:999 data/rabbitmq
```

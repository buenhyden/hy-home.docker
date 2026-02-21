---
description: Start Local Development Environment via Docker Compose
---

1. **Check Docker Status**

    Ensure Docker Daemon is running.

    ```bash
    docker info
    ```

2. **Start Services**

    Run `docker-compose up` in detached mode.

    // turbo

    ```bash
    docker-compose up -d
    ```

3. **Show Logs**

    Follow the logs to ensure services started correctly.

    // turbo

    ```bash
    docker-compose logs -f
    ```

4. **Tear Down (Optional)**

    To stop and remove containers: `docker-compose down`

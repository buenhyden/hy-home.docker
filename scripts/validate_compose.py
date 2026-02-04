import os
import subprocess
import sys


def main():
    files = sys.argv[1:]
    has_error = False

    root_compose = "docker-compose.yml"
    root_exists = os.path.exists(root_compose)

    root_content = ""
    if root_exists:
        try:
            with open(root_compose, "r", encoding="utf-8") as f:
                root_content = f.read()
        except Exception:
            # Fallback if reading fails
            root_exists = False

    # Load environment variables from .env or .env.example
    env_vars = os.environ.copy()

    # Try to load from .env first, then .env.example
    dotenv_files = [".env", ".env.example"]
    for env_file in dotenv_files:
        if os.path.exists(env_file):
            try:
                with open(env_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            if key not in env_vars:
                                env_vars[key] = value
            except Exception as e:
                print(f"Warning: Failed to load {env_file}: {e}")

    # Dummy defaults for common variables that cause validation failures
    dummy_defaults = {
        "HTTP_HOST_PORT": "80",
        "HTTP_PORT": "80",
        "HTTPS_HOST_PORT": "443",
        "HTTPS_PORT": "443",
        "TRAEFIK_DASHBOARD_HOST_PORT": "8080",
        "TRAEFIK_DASHBOARD_PORT": "8080",
        "TRAEFIK_METRICS_HOST_PORT": "9100",
        "TRAEFIK_METRICS_PORT": "9100",
        "DEFAULT_URL": "localhost",
        "AIRFLOW_PORT": "8080",
        "FLOWER_PORT": "5555",
        "STATSD_AIRFLOW_PORT": "9125",
        "STATSD_PROMETHEUS_PORT": "9102",
        "REDIS_PASSWORD": "dummy",
        "AIRFLOW_UID": "50000",
        "INFRA_SUBNET": "172.19.0.0/16",
        "INFRA_GATEWAY": "172.19.0.1",
        "POSTGRES_HOSTNAME": "localhost",
        "POSTGRES_PORT": "5432",
        "REDIS_NODE_NAME": "localhost",
        "REDIS_PORT": "6379",
        "STATSD_HOST": "localhost",
        "AIRFLOW_DB_USER": "airflow",
        "AIRFLOW_DB_PASSWORD": "dummy",
        "AIRFLOW_IMAGE_NAME": "apache/airflow:latest",
    }

    for key, value in dummy_defaults.items():
        if key not in env_vars:
            env_vars[key] = value

    # Explicitly set COMPOSE_INTERACTIVE_NO_CLI to avoid issues in CI
    env_vars["COMPOSE_INTERACTIVE_NO_CLI"] = "1"

    for f in files:
        # Normalize path separators for checking against docker-compose.yml content
        f_normalized = f.replace("\\", "/")

        cmd = []
        if root_exists:
            # Check if file is already included in root compose
            # naive check: strict substring match of the relative path
            if f_normalized in root_content:
                # Validate via root (validates includes too)
                cmd = ["docker", "compose", "-f", root_compose, "config", "-q"]
            else:
                # Validate by extending root
                cmd = ["docker", "compose", "-f", root_compose, "-f", f, "config", "-q"]
        else:
            cmd = ["docker", "compose", "-f", f, "config", "-q"]

        try:
            subprocess.run(cmd, check=True, capture_output=True, env=env_vars)
            # print(f"Passed: {f}") # Optional: verify pass
        except subprocess.CalledProcessError as e:
            print(f"Validation failed for {f}:")
            print(e.stderr.decode().strip())
            has_error = True
        except FileNotFoundError:
            print(
                "Error: 'docker' command not found. Please ensure Docker is installed and in your PATH."
            )
            sys.exit(1)

    sys.exit(1 if has_error else 0)


if __name__ == "__main__":
    main()

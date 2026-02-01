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
            subprocess.run(cmd, check=True, capture_output=True)
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

import os
import glob

# Files to fix MD001 (### Context -> ## Context)
target_files = [
    "docs/guides/infra-migrated-setup.md",
    "operations/infra-migrated-operations.md",
    "runbooks/infra-migrated-troubleshooting.md"
]

for fp in target_files:
    if os.path.exists(fp):
        with open(fp, 'r') as f:
            content = f.read()

        # Replace ### Context: with ## Context:
        content = content.replace("### Context:", "## Context:")

        # Fix the specific MD051 fragment link
        if "infra-migrated-troubleshooting.md" in fp:
            content = content.replace("[Configuration](#kernel-requirements-important)", "Configuration")

        with open(fp, 'w') as f:
            f.write(content)

print("Fixed MD001/MD051 lint errors.")

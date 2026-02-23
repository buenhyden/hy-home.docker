import os
import re

files_to_fix = [
    "runbooks/auth-lockout.md",
    "docs/guides/vault-setup.md",
    "runbooks/vault-sealed.md",
    "operations/minio-operations.md",
    "runbooks/minio-sync-failure.md",
    "runbooks/kafka-broker-offline.md"
]

def renumber_lists(filepath):
    if not os.path.exists(filepath):
        return

    with open(filepath, 'r') as f:
        lines = f.readlines()

    out_lines = []
    current_list_num = 1
    in_list = False

    for line in lines:
        match = re.match(r'^(\s*)\d+\.\s+(.*)', line)
        if match:
            indent = match.group(1)
            content = match.group(2)
            out_lines.append(f"{indent}{current_list_num}. {content}\n")
            current_list_num += 1
            in_list = True
        else:
            if line.strip() == "":
                # Could be a break in the list or just a newline
                pass
            elif not re.match(r'^\s+', line) and not line.startswith('#'):
                # Reset counter if we hit a normal non-indented line that isn't a header,
                # but only if it's clearly breaking the context.
                pass

            if re.match(r'^#', line):
                 current_list_num = 1

            out_lines.append(line)

    with open(filepath, 'w') as f:
        f.writelines(out_lines)

for fp in files_to_fix:
    renumber_lists(fp)

print("Markdown lists reformatted.")

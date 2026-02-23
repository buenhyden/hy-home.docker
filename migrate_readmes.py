import os
import glob
import re

readme_files = glob.glob('infra/**/README.md', recursive=True)

pointer_template = """# {title}

> **Note**: This component's local documentation has been migrated to the global repository standards to enforce Spec-Driven Development boundaries.

Please refer to the following global documentation directories for information regarding this service:
- **Architecture & Topology**: [docs/architecture](../../../docs/architecture)
- **Configuration & Setup Guides**: [docs/guides](../../../docs/guides)
- **Routine Operations**: [operations/](../../../operations)
- **Troubleshooting & Recovery**: [runbooks/](../../../runbooks)
"""

def extract_sections(content):
    # Regex to split by H2
    sections = re.split(r'\n## ', '\n' + content)
    parsed = {}
    title = "Infrastructure Component"

    # Extract H1 Title
    m_title = re.search(r'^#\s+(.*)', content, re.MULTILINE)
    if m_title:
        title = m_title.group(1).strip()

    for sec in sections:
        if not sec.strip() or sec.startswith('# '):
            continue
        lines = sec.split('\n', 1)
        if len(lines) == 2:
            sec_title = lines[0].strip().lower()
            sec_body = "## " + lines[0] + "\n" + lines[1]
            parsed[sec_title] = sec_body

    return title, parsed

arch_content = []
guide_content = []
ops_content = []
runbook_content = []

for fp in readme_files:
    if fp.count(os.sep) < 1: continue

    with open(fp, 'r') as f:
        content = f.read()

    # Skip already migrated ones
    if "migrated to the global repository standards" in content:
        continue

    title, sections = extract_sections(content)

    comp_name = os.path.basename(os.path.dirname(fp))
    if comp_name == "infra" or comp_name.startswith("0"):
        comp_name = fp.split(os.sep)[1]

    # Map content based on keywords
    for sec_title, sec_body in sections.items():
        block = f"\n\n### Context: {title} ({comp_name})\n{sec_body}"

        if 'overview' in sec_title or 'mermaid' in sec_body or 'architecture' in sec_title:
            arch_content.append(block)
        elif 'troubleshoot' in sec_title or 'error' in sec_title or 'fail' in sec_title:
            runbook_content.append(block)
        elif 'usag' in sec_title or 'operat' in sec_title or 'run' in sec_title or 'maintain' in sec_title:
            ops_content.append(block)
        else: # config, services, persistence, network, etc
            guide_content.append(block)

    # Rewrite the README to pointer
    with open(fp, 'w') as f:
        ptr = pointer_template.format(title=title)
        # Fix relative links depending on depth
        depth = fp.count(os.sep)
        ups = "../" * depth
        ptr = ptr.replace("../../../", ups)
        f.write(ptr)


def append_to_file(filepath, header, blocks):
    if not blocks: return
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    mode = 'a' if os.path.exists(filepath) else 'w'
    with open(filepath, mode) as f:
        if mode == 'w':
            f.write(f"# {header}\n")
        f.write("\n\n<!-- MIGRATED CONTENT BELOW -->\n")
        f.write("\n".join(blocks))

append_to_file("docs/architecture/infra-migrated-architecture.md", "Migrated Infra Architecture & Topologies", arch_content)
append_to_file("docs/guides/infra-migrated-setup.md", "Migrated Infra Configuration & Setup", guide_content)
append_to_file("operations/infra-migrated-operations.md", "Migrated Infra Routine Operations", ops_content)
append_to_file("runbooks/infra-migrated-troubleshooting.md", "Migrated Infra Troubleshooting", runbook_content)

print(f"Migration completed for {len(readme_files)} files.")

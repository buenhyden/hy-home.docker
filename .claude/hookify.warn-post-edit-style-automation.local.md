---
name: warn-post-edit-style-automation
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.(md|sh|ya?ml|json)$
action: warn
---

**Post-edit style automation**

After this edit, the shared PostToolUse hook may normalize changed text files
and run changed-file style checks:

- trims trailing spaces and ensures newline at EOF for Markdown, shell, YAML,
  and JSON files
- runs `shfmt -w` and `shfmt -d` for changed hook/script shell files when
  `shfmt` is available
- runs `shellcheck` for changed hook/script shell files when available
- runs `yamllint -c .yamllint` for changed YAML files when available
- runs `git diff --check` for changed files before repository validators

Inspect the resulting diff before committing.

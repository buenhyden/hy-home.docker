# Library tests

`tests/lib/<domain>/` mirrors the primary responsibility of
`scripts/lib/<domain>/`. Each library domain has a matching test directory;
cross-domain validation and entrypoint behavior remain under
`tests/validation/`.

A matching directory must contain a tracked behavior test registered in the
public full profile. An empty directory, local bytecode cache, placeholder or
untracked test is not ownership evidence. The Script Manifest connects each
library to its behavioral tests; full-profile checks retain exactly-once module
execution.

These directories are implicit namespace packages. Do not add `__init__.py`;
registered suites use their exact dotted module names.

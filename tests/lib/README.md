# Library tests

`tests/lib/<domain>/` mirrors the primary responsibility of
`scripts/lib/<domain>/`. Each library domain has a matching test directory;
cross-domain validation and entrypoint behavior remain under
`tests/validation/`.

These directories are implicit namespace packages. Do not add `__init__.py`;
registered suites use their exact dotted module names.

"""Validate Iceberg tables through Trino against tracked expectation suites.

A suite file `<name>.json` holds GX expectations plus the table it checks:
{"name": "<name>", "table": "<schema>.<table>", "expectations": [{"type": ..., "kwargs": {...}}]}.
`list` prints the suites; `validate NAME...` checks them (all when no name).
Exit 0: every suite passed. Exit 1: an expectation failed. Exit 2: the run
could not check (bad suite, no suites, Trino error). Nothing is written.
"""

import json
import os
import pathlib
import sys

SUITES = pathlib.Path("/opt/hyhome/suites")


def fail(message: str) -> None:
    print(f"great-expectations: {message}", file=sys.stderr)
    sys.exit(2)


def load(name: str) -> dict:
    path = SUITES / f"{name}.json"
    if not path.is_file():
        fail(f"no suite {name!r} in {SUITES}")
    try:
        spec = json.loads(path.read_text(encoding="utf-8"))
        parts = spec["table"].split(".")
        expectations = spec["expectations"]
    except (ValueError, KeyError, AttributeError) as error:
        fail(f"{name}: malformed suite ({error})")
    if spec.get("name", name) != name:
        fail(f"{name}: name {spec['name']!r} does not match the file name")
    if len(parts) != 2 or not all(parts) or not expectations:
        fail(f"{name}: needs table <schema>.<table> and at least one expectation")
    return spec


def validate(names: list[str]) -> int:
    specs = {name: load(name) for name in names}
    import great_expectations as gx
    from great_expectations.data_context.types.base import ProgressBarsConfig
    from great_expectations.expectations.expectation_configuration import (
        ExpectationConfiguration,
    )

    context = gx.get_context(mode="ephemeral")
    context.variables.progress_bars = ProgressBarsConfig(globally=False)
    source = context.data_sources.add_sql(
        name="lakehouse", connection_string=os.environ["GX_TRINO_URL"]
    )
    failed = 0
    for name, spec in specs.items():
        schema, table = spec["table"].split(".")
        asset = source.add_table_asset(name=name, table_name=table, schema_name=schema)
        suite = context.suites.add(gx.ExpectationSuite(name=name))
        for item in spec["expectations"]:
            suite.add_expectation_configuration(
                ExpectationConfiguration(type=item["type"], kwargs=item.get("kwargs", {}))
            )
        batch = asset.add_batch_definition_whole_table("all").get_batch()
        result = batch.validate(suite)
        for r in result.results:
            print(
                json.dumps(
                    {
                        "suite": name,
                        "expectation": r.expectation_config.type,
                        "kwargs": r.expectation_config.kwargs,
                        "success": r.success,
                    },
                    default=str,
                )
            )
        print(json.dumps({"suite": name, "table": spec["table"], "success": result.success}))
        failed += not result.success
    return 1 if failed else 0


def main(argv: list[str]) -> int:
    names = sorted(p.stem for p in SUITES.glob("*.json"))
    if not names:
        fail(f"no suites in {SUITES}")
    if argv[:1] == ["list"]:
        print("\n".join(names))
        return 0
    if argv[:1] == ["validate"]:
        try:
            return validate(argv[1:] or names)
        except SystemExit:
            raise
        except Exception as error:  # Trino, GX or an unknown expectation type
            fail(f"{type(error).__name__}: {error}")
    fail("usage: hyhome-gx list | validate [SUITE...]")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

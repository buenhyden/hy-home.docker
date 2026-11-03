from __future__ import annotations

from . import tools


def register(ctx) -> None:
    tools._CTX = ctx
    ctx.register_tool(
        name="collect_research_source",
        toolset="research_report",
        schema=tools.COLLECT_RESEARCH_SOURCE_SCHEMA,
        handler=tools.handle_collect_source,
    )
    ctx.register_tool(
        name="submit_research_report",
        toolset="research_report",
        schema=tools.SUBMIT_RESEARCH_REPORT_SCHEMA,
        handler=tools.handle_submit_report,
    )

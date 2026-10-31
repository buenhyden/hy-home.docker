from __future__ import annotations

from . import tools


def register(ctx) -> None:
    ctx.register_tool(
        name="submit_research_report",
        toolset="research_report",
        schema=tools.SUBMIT_RESEARCH_REPORT_SCHEMA,
        handler=tools.handle_submit_report,
    )

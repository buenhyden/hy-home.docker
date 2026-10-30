"""Fail-closed dispatch policy until producer evidence can be authenticated."""

from .candidates import JOBS


def evidence_required(job_id):
    """The admitted Hermes jobs have no verified-evidence promotion yet."""
    return job_id in JOBS

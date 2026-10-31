"""Jobs whose dispatch requires producer-authenticated evidence."""

from .candidates import JOBS


def evidence_required(job_id):
    """Every admitted Hermes job needs evidence accepted by trust.authorize."""
    return job_id in JOBS

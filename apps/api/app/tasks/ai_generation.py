"""
Celery tasks for AI generation.
To be implemented in Phase 3.
"""
from app.tasks.celery_app import celery_app


@celery_app.task(name="generate_cv")
def generate_cv_task(user_id: str, job_id: str, options: dict):
    """
    Generate CV for a job application.
    Implementation coming in Phase 3.
    """
    # TODO: Implement in Phase 3
    return {"status": "not_implemented", "message": "Coming in Phase 3"}


@celery_app.task(name="generate_cover_letter")
def generate_cover_letter_task(user_id: str, job_id: str, options: dict):
    """
    Generate cover letter for a job application.
    Implementation coming in Phase 3.
    """
    # TODO: Implement in Phase 3
    return {"status": "not_implemented", "message": "Coming in Phase 3"}

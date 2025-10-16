"""
Celery tasks for job scraping.
To be implemented in Phase 4.
"""
from app.tasks.celery_app import celery_app


@celery_app.task(name="scrape_jobs")
def scrape_jobs_task(user_id: str, sources: list, preferences: dict):
    """
    Scrape jobs from multiple sources.
    Implementation coming in Phase 4.
    """
    # TODO: Implement in Phase 4
    return {"status": "not_implemented", "message": "Coming in Phase 4"}

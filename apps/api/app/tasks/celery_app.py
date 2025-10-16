"""
Celery application configuration.
"""
from celery import Celery
from app.config import settings

# Create Celery app
celery_app = Celery(
    "job_app_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Celery configuration
celery_app.conf.update(
    task_track_started=settings.CELERY_TASK_TRACK_STARTED,
    task_time_limit=settings.CELERY_TASK_TIME_LIMIT,
    result_expires=3600,  # 1 hour
    accept_content=["json"],
    task_serializer="json",
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Auto-discover tasks in these modules
    imports=[
        "app.tasks.scraping",
        "app.tasks.ai_generation",
    ],
)

# Optional: Configure periodic tasks with Celery Beat
celery_app.conf.beat_schedule = {
    # Example: Run job scraping daily at 9 AM
    # "daily-job-scraping": {
    #     "task": "app.tasks.scraping.scheduled_scrape",
    #     "schedule": crontab(hour=9, minute=0),
    # },
}

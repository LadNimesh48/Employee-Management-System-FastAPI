from app.core.celery_app import celery_app
from app.utils.email import send_welcome_email, TemppraryEmailError


@celery_app.task(bind=True, name="send_welcome_email", max_retries=3)
def send_welcome_email_task(self, email:str, name: str):
    try:
        send_welcome_email(email, name)
        
        return ("Welcome Email has been sent Successfully")
    
    except TemppraryEmailError as e:
        raise self.retry(exc=e, countdown=10)
    
    except Exception as e:
        raise
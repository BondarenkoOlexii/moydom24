import os
from celery import Celery
import redis
from celery import shared_task
from django.core.mail import EmailMessage, get_connection


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

#@app.task(bind=True)
#def debug_task(self):
   # print(f'Request: {0!r}'.format(self.request))

@shared_task(bind=True)
def send_invite_email(self, subject, message, email_from, email_to):

    connection = get_connection()
    connection.open()
    try:
        invite_msg = EmailMessage(
            subject=subject,
            body=message,
            from_email=email_from,
            to=[email_to],
            connection=connection
        )

        invite_msg.content_subtype = "html"

        invite_msg.send()

    except Exception as e:
        print(e)

    finally:
        connection.close()




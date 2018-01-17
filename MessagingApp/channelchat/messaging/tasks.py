from celery.task.schedules import crontab
from celery.decorators import periodic_task, task
from celery.utils.log import get_task_logger

from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail

from messaging.models import Message

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(hour='0')),
    name="send_email_reminder",
)
def send_email_reminder():
    """
        Send email reminder for unread messages every 12AM
    """
    latest_messages = Message.objects.order_by(
        'conversation', '-pk').distinct('conversation')
    for message in latest_messages:
        unseen_users = message.unseen_by.exclude(email="")
        send_mail(
            'ChannelChat: Reminder',
            'You have unread messages. ',
            settings.EMAIL_HOST_USER,
            unseen_users.values_list('email', flat=True),
            fail_silently=False,
        )
    return "email reminder sent!"

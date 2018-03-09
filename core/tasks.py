import celery
import threading

from celery.utils.log import get_task_logger
from django.core.mail import EmailMessage
from django.conf import settings
from utils.string_utils import valid_email

logger = get_task_logger(__name__)


@celery.task(default_retry_delay=2 * 10, max_retries=2)
def email(to, subject, message):
    """
    Sends email to user/users. 'to' parameter must be a string or list.
    """
    # Converto to list if one user's email is passed
    if not isinstance(to, list):  # Python 2.x only
        to = [to]
    try:
        email_list = list(filter(lambda email: valid_email(email), to))
        # msg = EmailMessage(subject, message,
        #                    from_email=settings.FROM_EMAIL,
        #                    to=email_list)
        # msg.content_subtype = "html"
        # msg.send()
        send_html_mail(subject, message, to)
    except Exception as exc:
        print(exc)
        raise email.retry(exc=exc)


class EmailThread(threading.Thread):

    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(
            self.subject, self.html_content,
            from_email=settings.FROM_EMAIL, to=self.recipient_list)
        msg.content_subtype = "html"
        msg.send()


def send_html_mail(subject, html_content, recipient_list):
    EmailThread(subject, html_content, recipient_list).start()

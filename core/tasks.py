import celery
import threading

from celery.utils.log import get_task_logger
from django.core.mail import EmailMessage
from django.conf import settings

from core.models import Exchange
from utils.string_utils import valid_email

from celery.task import periodic_task

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


numbers = []
for x in range(0, 10):
    numbers.append(str(x))

doubles = numbers
doubles.append(".")


def clear_rate(current_rate):
    """
        Gets rid of commas in numbers inside the string
    """
    while "," in current_rate:
        ind = current_rate.find(",")
        current_rate = current_rate[:ind] + current_rate[(ind + 1):]
    return current_rate


def convert_to_list_rate(current_rate):
    """
        Gets list of organized floats from the string
    """
    current_rate = current_rate[55:]
    my_list = []
    head = -1
    tail = -1
    for i in range(5):
        for j in range(len(current_rate)):
            if current_rate[j] in doubles:
                head = j
                break

        for j in range(head + 1, len(current_rate)):
            if current_rate[j] not in doubles:
                tail = j - 1
                break

        number = current_rate[head: (tail + 1)]
        my_list.append(float(number))
        current_rate = current_rate[(tail + 1):]
    return my_list


# @periodic_task()
@celery.task(default_retry_delay=5, max_retries=None)
def converter_task():
    """
    update info each period of time.
    converter task
    """
    import requests
    url = 'http://english.visitseoul.net/exchange'
    r = requests.get(url)
    source_bytes = r.content
    source = source_bytes.decode("utf-8")
    new_source = source[(source.index("Provided by Woori Bank") - 25):(source.index("Australian Dollar</td>") - 53)]
    current_rate = new_source[(len(new_source) - 180):]
    current_time = new_source[1:25]
    new_current_time = current_time[:10] + " " + current_time[(len(current_time) - 8):]

    ind = len(current_rate) - 1
    while current_rate[ind] not in numbers:
        ind = ind - 1
    ind_end = ind
    while current_rate[ind_end] is not '>':
        ind_end = ind_end - 1

    current_rate = clear_rate(current_rate)

    my_list = convert_to_list_rate(current_rate)
    exchange = Exchange.objects.create(sending=my_list[len(my_list) - 2],
                                       receiving=my_list[len(my_list) - 1],
                                       data_and_time=new_current_time)
    # final_dict = {
    #     "data_and_time": new_current_time,
    #     "sending": my_list[len(my_list) - 2],
    #     "receiving": my_list[len(my_list) - 1],
    # }
    # return final_dict


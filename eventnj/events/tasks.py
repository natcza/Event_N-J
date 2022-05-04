# # # Create your tasks here
from config.celery import app
# from time import sleep
#
# from django.core.mail import send_mail
#
# @app.task(bind=True)
# def test(param):
#     return 'The test task executed with argument "%s" ' % param
#
# # def send_email_delay():
# #     sleep(10)
# #     send_mail("Celery Task Worked",
# #     "This is proof the task worked!",
# #     "from@example.com",
# #     ['natcza612@gmail.com'])
# #     return None
# #
# # @app.task(bind=True)
# # def send_email_task():
# #     send_email_delay()
# #     # sleep(10)
# #     # send_mail("Celery Task Worked",
# #     # "This is proof the task worked!",
# #     # "from@example.com",
# #     # ['natcza612@gmail.com'])
# #     # return None

# from celery.decorators import task
from celery.utils.log import get_task_logger
from time import sleep
logger = get_task_logger(__name__)

@app.task(name='my_first_task')
def my_first_task(duration):
    sleep(duration)
    return('first_task_done')
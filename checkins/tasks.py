from celery import shared_task

@shared_task
def send_reminder():
    print('foo')

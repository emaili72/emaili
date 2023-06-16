from celery import shared_task
from django.core.mail import send_mail
from decouple import config


@shared_task
def send_activation_code(email, activation_code):
    activation_link = f'http://{config("SERVER_CONFIG")}/account/activate/{activation_code}/'
    message = f'Активируйте аккаунт перейдя по ссылке {activation_link}\nВнимание! '
    send_mail('Activate account', message, 'admin@admin.com', [email])
    return 'Send'
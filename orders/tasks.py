from celery import shared_task
from django.core.mail import send_mail
from .models import Order


# pip install flower
# celery -A myshop worker -l info - запуск воркера
# celery -A myshop flower - запуск flower мониторинг задач, localhost:5555

@shared_task
def order_created(order_id):
    """
    Асинхронное задание по отправке уведомления по почте
    при успешной создании заказа
    """

    order = Order.objects.get(id=order_id)
    subject = f'Закак номер {order.id}'
    message = f'Уважаемый {order.first_name}, \n\nВаш заказ успешно создан. Номер заказа: {order.id}'
    mail_sent = send_mail(
        subject,
        message,
        'admin@myshop.com',
        [order.email],
    )
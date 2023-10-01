from django.db.models.signals import post_save
from django.core.mail import send_mail

from orders.models import Order
from customers.models import Customer
from .models import Robot
from django.conf import settings


# Отправка обычного письма





def save_robot(sender, **kwargs):
    orders = Order.objects.filter(robot_serial=kwargs['instance'].serial).filter(status='w')
    if kwargs['instance'].status == 'g' and orders:
        customers = set()
        for o in orders:
            customers.add(o.customer.email)
            o.status = 'e'
            o.save()
        temlate_test = f'Добрый день!\nНедавно вы интересовались нашим роботом модели {kwargs["instance"].model}, версии {kwargs["instance"].version}. Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами'
        send_mail('Robot Manufacturer', temlate_test, settings.EMAIL_HOST_USER,  list(customers))

post_save.connect(save_robot, sender=Robot)


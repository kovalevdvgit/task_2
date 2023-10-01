from django.db import models

from customers.models import Customer


class Order(models.Model):
    tuple_status =(
        ('w', 'Ожидает получения робота'),
        ('g', 'Передан в упаковочный цех'),
        ('e', 'Передали письмо о наличие робота'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5, blank=False, null=False)
    #Для реализации логики с отправкой письма
    status = models.CharField(max_length=1, choices=tuple_status, default='w')


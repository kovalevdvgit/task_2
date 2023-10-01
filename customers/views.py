from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Customer
from robots.models import Robot
from orders.models import Order


import json


@csrf_exempt
def for_customers(request):
    data_json = json.loads(request.body)
    base_keys = ["email", "robot_serial"]

    if list(data_json.keys()) == base_keys:

        if data_json['robot_serial'][2] != '-' or len(data_json['robot_serial']) != 5:
            return JsonResponse({'message': 'Дорогой заказчик вы передали не допустимую серию робота! Формат серии должен быть -> Модель(2 символа!)-Версия(2 символа!). Пример RD-D2'})

        try:
            customer = Customer.objects.get(email=data_json['email'])
        except:
            customer = Customer(email=data_json['email'])
            customer.save()


        oder = Order(customer=customer, robot_serial = data_json['robot_serial'])

        try:
            robot = Robot.objects.filter(serial = data_json['robot_serial']).filter(status='g')[0]
            robot.status = 'p'
            robot.save()

            oder.status = 'r'
            oder.save()

            return JsonResponse({'message': 'Робот по вашему заказу будет скоро доставлен'})
        except:
            oder.status = 'w'
            oder.save()
            return JsonResponse({'message': 'Дорогой заказчик настоящий момент у на нет данного работа в наличие(, как только он появится мы сообщим вам по почте'})

    else:
        return JsonResponse({'message': 'Дорогой заказчик вы передали не корректные данные! Формат данных должен быть {"email":Ваш email, "robot_serial": Серия требуемого робота}'})


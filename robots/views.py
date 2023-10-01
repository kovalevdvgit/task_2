from django.shortcuts import render

from robots.models import Robot

from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
import pandas as pd

# Create your views here.
@csrf_exempt
#Отключил проверку csrf token для проверки легкой проверки тип requests.post('http://localhost:8000/add_robot/', json{'key':'value'})!!!
def add_new_robot(request):
    try:
        data_json = json.loads(request.body)
        base_keys = ["model", "version", "created"]
        if list(data_json.keys()) == base_keys:
            serial = '-'.join([str(data_json['model']), str(data_json['version'])])

            if serial[2] != '-' or len(serial) != 5:
                return JsonResponse({'Формат серии должен быть -> Модель(2 символа!)-Версия(2 символа!). Пример RD-D2'})

            try:
                created = datetime.strptime(data_json["created"], '%Y-%m-%d %H:%M:%S')
                if created > datetime.now():
                    return JsonResponse({'message': 'Не используйти будующую временныю метку!'})
                robot = Robot(serial=serial, model=str(data_json['model']), version=str(data_json['version']), created=created)
                robot.save()
            except:
                return JsonResponse({'message': 'Переданны не корректные данные. Пример правильных данных -> "model": "R2", "version": "D2", "created": "2022-12-31 23:59:59"'})
            return JsonResponse({'message': 'Робот успешно добавден в БД'})
        else:
            return JsonResponse({'message': 'Не правильный структура данных. Пример прафилоьной структуры {"model":str, "version":str, "created":str}'})
    except:
        return JsonResponse({'message': 'Не правильный формат переданых данных. Данные должны быть передыны в формате JSON'})

def make_report(request):

    set_model = set()
    [set_model.add(i.model) for i in Robot.objects.all()]

    dict_set_model_version = {}

    for s in set_model:
        dict_set_model_version[s] =  list(set([i.version for i in Robot.objects.filter(model=s)]))

    kol_model = []
    kol_version = []
    kol_shtuk = []

    machine = pd.ExcelWriter('./document.xlsx', engine='xlsxwriter')

    for m in dict_set_model_version.keys():
        for v in dict_set_model_version[m]:

            robots = Robot.objects.filter(model=m).filter(version=v)
            schetchik = 0
            for r in robots:
                if (datetime.now() - r.created).days <= 7:
                    print(datetime.now() - r.created)
                    schetchik += 1
            kol_model.append(m)
            kol_version.append(v)
            kol_shtuk.append(schetchik)
            print(m, v, schetchik)
        print(kol_model, kol_version, kol_shtuk)

        doc = pd.DataFrame({'Модель': kol_model,
                   'Версия': kol_version,
                   'Количество за неделю': kol_shtuk})
        doc.to_excel(machine, sheet_name=m, index=False)

        kol_model.clear()
        kol_version.clear()
        kol_shtuk.clear()

    machine._save()

    return FileResponse(open('document.xlsx', 'rb'))





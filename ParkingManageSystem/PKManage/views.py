import json
import math

import pytz
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import requests
import base64
import datetime
from PKManage import models
from PKManage.models import Car,Position

Access_token = ''

def recommand():
    Position_list = models.Position.objects.all()
    # Find the max value of range
    distance_range = 1
    for position in Position_list:
        if position.distance > distance_range:
            distance_range = position.distance
    recommand = distance_range
    for position in Position_list:
        if position.distance == recommand:
            recommand_position = models.Position.objects.get(positionid=position.positionid)
            break
    for i in range(1, recommand+1):
        for position in Position_list:
            if position.distance <= i and position.distance>0:
                if position.status == False:
                    recommand_position = models.Position.objects.get(positionid=position.positionid)
                    return recommand_position
    return models.Position.objects.get(positionid='Test')


@csrf_exempt
def Listall(request):
    Car_list = models.Car.objects.all()
    Time = datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))
    recommandsite = recommand()
    for car in Car_list:
        Difference = (Time - car.Time).days*24 + (Time - car.Time).seconds/3600
        Difference = math.ceil(Difference)
        car.Charge = Difference*5
        if(car.Counter%2==0):
            car.Charge = 0
            car.save()
    return HttpResponse(render(request, 'Mainpage.html',{'recommand':recommandsite,'Car_list' : Car_list}))


def access():
    global Access_token
    # Please get your own API acess token in Baidu intelligent cloud.
    host = ''
    response = requests.get(host)
    if response:
         Access_token = json.loads(response.text)


@csrf_exempt
def CarRegister(request):
    return HttpResponse(render(request,'CarRegister.html'))


@csrf_exempt
def recognition(request):
    access()
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/license_plate"
    # 二进制方式打开图片文件
    pic = request.FILES['pic']
    img = base64.b64encode(pic.read())
    params = {"image":img}
    access_token = Access_token['access_token']
    request_url = str(request_url) + "?access_token=" + str(access_token)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        CarInfo = response.json()
        print(CarInfo)
        License = CarInfo['words_result']['number']
        Time = datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))
        pos = recommand()
        if models.Car.objects.filter(License=License):
            oldcar = Car.objects.get(License=License)
            oldcar.Counter +=1
            if oldcar.Position.status == False:
                models.Position.objects.filter(positionid=oldcar.Position.positionid).update(status=True)
            else:
                models.Position.objects.filter(positionid=oldcar.Position.positionid).update(status=False)
            oldcar.save()
        else:
            if pos.status == False:
                models.Position.objects.filter(positionid=pos.positionid).update(status=True)
            else:
                models.Position.objects.filter(positionid=pos.positionid).update(status=False)
            Car.objects.create(License=License,Time=Time,Counter=1,Position=pos,Charge=0)
    Car_list = models.Car.objects.all()
    Time = datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))
    for car in Car_list:
        Difference = (Time - car.Time).days * 24 + (Time - car.Time).seconds / 3600
        Difference = math.ceil(Difference)
        car.Charge = Difference * 5
        car.save()
        if (car.Counter % 2 == 0):
            car.Charge = 0
            car.save()
    recommandsite = recommand()
    return HttpResponse(render(request, 'Mainpage.html',{'recommand':recommandsite,'Car_list' : Car_list}))


@csrf_exempt
def Search(request):
    return HttpResponse(render(request,'Search.html'))


@csrf_exempt
def searching(request):
    q = request.GET.get('search')
    car = Car.objects.get(License=q)
    Time = datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))
    Difference = (Time - car.Time).days * 24 + (Time - car.Time).seconds / 3600
    Difference = math.ceil(Difference)
    car.Charge = Difference * 5
    car.save()
    return HttpResponse(render(request,'Result.html',{'car_result':car}))


@csrf_exempt
def Report(request):
    return HttpResponse(render(request,'Report.html'))

@csrf_exempt
def report(request):
    q = request.GET.get('report')
    send_mail(subject='parking charging system report',
              message = q,
              # Please enter your own email address.
              from_email='',
              recipient_list=[''],
              fail_silently=False)
    messages.success(request,"The information is published successfully. The administrator will check and modify the error information")
    Car_list = models.Car.objects.all()
    Time = datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))
    recommandsite = recommand()
    for car in Car_list:
        Difference = (Time - car.Time).days * 24 + (Time - car.Time).seconds / 3600
        Difference = math.ceil(Difference)
        car.Charge = Difference * 5
        if (car.Counter % 2 == 0):
            car.Charge = 0
    return HttpResponse(render(request, 'Mainpage.html', {'recommand': recommandsite, 'Car_list': Car_list}))





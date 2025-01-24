from django.http import HttpResponse
from django.shortcuts import render, redirect


def Homepage(request):
    return render(request, 'Homepage.html')


def application(request):
    return render(request, 'application.html')


def faults(request):
    return render(request, 'faults.html')


def connect_us(request):
    return render(request, 'connect_us.html')


def Personal_erea(request):
    return render(request, 'Personal_erea.html')


def manager_Homepage(request):
    return render(request, 'manager_Homepage.html')


def BM_Homepage(request):
    return render(request, 'BM_Homepage.html')


def Students_homepage(request):
    return render(request, 'Students_homepage.html')


def BM_faults(request):
    return render(request, 'BM_faults.html')


def BM_sendMassage(request):
    return render(request, 'BM_sendMassage.html')


def manage_room(request):
    return render(request, 'manage_room.html')


def manager_inventory(request):
    return render(request, 'manager_inventory.html')


def manager_BM(request):
    return render(request, 'manager_BM.html')



def Manager_request(request):
    return render(request, 'Manager_request.html')



def manager_faults(request):
    return render(request, 'manager_faults.html')


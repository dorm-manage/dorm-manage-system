from django.http import HttpResponse
from django.shortcuts import render, redirect

def index(request):
    return render(request, 'index.html')


def application(request):
    return render(request, 'application.html')


def faults(request):
    return render(request, 'faults.html')


def connect_us(request):
    return render(request, 'connect_us.html')
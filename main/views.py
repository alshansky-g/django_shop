from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    ...


def about(request):
    return HttpResponse('Информация о нас')

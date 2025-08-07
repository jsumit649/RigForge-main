from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'core/home.html')

def build(request):
    return render(request, 'core/build.html')

def login(request):
    pass

def logout(request):
    pass
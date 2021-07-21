from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse

def helloworld(request):
    return HttpResponse("Ola mundo")
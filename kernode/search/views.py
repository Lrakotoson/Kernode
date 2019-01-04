from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render(request=request))

def results(request, search_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response %search_id)

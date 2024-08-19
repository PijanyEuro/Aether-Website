from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.



def main(request):
        template = loader.get_template('base_template.html')
        return HttpResponse(template.render())

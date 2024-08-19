from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# Balls


def main(request):
        return HttpResponse("balls", content_type="text/plain")

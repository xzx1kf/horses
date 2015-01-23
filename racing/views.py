from django.shortcuts import render

from racing.models import Meeting, Race, Horse


def index(request):
    return render(request, 'racing/index.html', {})

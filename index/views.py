from django.shortcuts import render


def index(request):
    username = 'Guest'
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, 'base.html', {'username': username})

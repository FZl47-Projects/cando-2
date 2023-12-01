from django.shortcuts import render


def err_403_handler(request, exception):
    return render(request, 'public/errors/403.html')


def err_404_handler(request, exception):
    return render(request, 'public/errors/404.html')


def err_500_handler(request):
    return render(request, 'public/errors/500.html')


def index(request):
    context = {

    }
    return render(request, 'public/index.html', context)

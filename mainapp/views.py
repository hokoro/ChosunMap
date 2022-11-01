from django.shortcuts import render

# Create your views here.

from django.shortcuts import render


# Create your views here.

def mainpage(request):
    return render(request, 'mainapp/mainpage.html')


def develop_info(request):
    return render(request, 'mainapp/developinfo.html')


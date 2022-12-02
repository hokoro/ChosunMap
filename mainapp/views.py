from django.shortcuts import render

# Create your views here.

from django.shortcuts import render


# Create your views here.
from mapapp.models import Mode


def mainpage(request):
    # convert Mode
    mo = Mode.objects.get(id=1)
    mo.mode = 1
    mo.save()

    return render(request, 'mainapp/mainpage.html')


def develop_info(request):
    return render(request, 'mainapp/developinfo.html')


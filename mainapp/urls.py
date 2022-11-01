from django.urls import path

from mainapp.views import mainpage, develop_info

app_name = 'mainapp'  # 만든것과 이름 똑같이

urlpatterns = [
    path('mainpage/', mainpage, name='mainpage'),
    path('developinfo/', develop_info, name='develop_info'),

]

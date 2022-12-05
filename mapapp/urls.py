from django.urls import path

from mapapp.views import SetMap, SearchCreateView, BusCreativeView

# from mapapp.views import Search

app_name = 'mapapp'  # 만든것과 이름 똑같이

urlpatterns = [
    path('setmap/', SetMap, name='map'),
    path('search/', SearchCreateView.as_view(), name='search'),
    path('bus/', BusCreativeView.as_view(), name='bus'),
]

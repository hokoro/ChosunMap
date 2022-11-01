from django.urls import path

from mapapp.views import SetMap, SearchCreateView

# from mapapp.views import Search

app_name = 'mapapp'  # 만든것과 이름 똑같이

urlpatterns = [
    path('setmap/',SetMap,name='map'),
    # path('search/',Search,name='search'),
    path('search/',SearchCreateView.as_view(),name='search'),
]

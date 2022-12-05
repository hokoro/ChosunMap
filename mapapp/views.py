from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView
from folium import plugins

# Create your views here.
from mapapp.forms import SearchCreationForm, BusCreationForm
from mapapp.map import Mapping
from mapapp.models import Building, Search, Mode, Search_Bus


def SetMap(request):
    mode = Mode.objects.get(id=1).mode  # 해당 버전이 어떤 버전인지 확인
    map_object = Mapping(mode)  # 클래스 객체 선언

    if mode == 1:  # mode -> Building DB
        names = Building.objects.values_list('name', flat=True)  # 건물 이름
        latitudes = Building.objects.values_list('latitude', flat=True)  # 건물의 위도
        longitudes = Building.objects.values_list('longitude', flat=True)  # 건물의 경도
        colors = Building.objects.values_list('color', flat=True)  # 아이콘의 색깔
        roles = Building.objects.values_list('role', flat=True)  # 아이콘의 모양
        prefixs = Building.objects.values_list('prefix', flat=True)  # 외부 아이콘 prefix 여부
        homepages = Building.objects.values_list('homepage', flat=True)  # homepage 주소
        map_object.Basicing(names, latitudes, longitudes, colors, roles, prefixs, homepages)
    if mode == 2:  # mode -> Search DB
        walk_count = Search.objects.count()
        departure = Search.objects.get(id=walk_count).departure  # 검색 DB 마지막 행 출발지
        arrival = Search.objects.get(id=walk_count).arrival  # 검색 DB 마지막 행 도착지
        if departure != arrival:  # 출발지 != 도착지
            map_object.Searching(departure, arrival)
        else:  # 출발지 == 도착지
            messages.add_message(request, messages.ERROR, "출발지와 목적지가 같습니다")  # django message framework ERROR
            return HttpResponseRedirect(reverse('mapapp:search'))  # 에러 즉시 Redirect 로 연결
    if mode == 3:  # mode -> Search_Bus
        bus_count = Search_Bus.objects.count()
        map_object.Bus(bus_count)

    chosunmap = map_object.getmap()
    plugins.LocateControl().add_to(chosunmap)
    plugins.Geocoder().add_to(chosunmap)
    maps = chosunmap._repr_html_()  # 지도를 템플릿에 삽입하기위해 iframe이 있는 문자열로 반환 (folium)

    return render(request, 'mapapp/map.html', {'map': maps})


class SearchCreateView(CreateView):
    model = Search  # html 에서 사용할 모델
    form_class = SearchCreationForm  # html 에 사용할 form
    # success_url = reverse_lazy('mapapp:map')
    template_name = 'mapapp/search.html'  # 해당 view 를 실행시킬 html

    def get_success_url(self):  # 해당 html 이 정상 실행 될떄 연결 시킬 url
        mo = Mode.objects.get(id=1)
        mo.mode = 2  # map mode = 2 Search
        mo.save()
        return reverse('mapapp:map')


class BusCreativeView(CreateView):
    model = Search_Bus  # html 에서 사용할 모델
    form_class = BusCreationForm  # html 에 사용할 form
    template_name = 'mapapp/bus.html'  # 해당 view 를 실행시킬 html

    def get_success_url(self):  # 해당 html 이 정상 실행 될떄 연결 시킬 url
        mo = Mode.objects.get(id=1)
        mo.mode = 3  # map mode = 3 Bus route
        mo.save()
        return reverse('mapapp:map')

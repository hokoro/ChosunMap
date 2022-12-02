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


def Message(request):
    return render(request, 'mapapp/message.html')


def SetMap(request):
    mode = Mode.objects.get(id=1).mode
    map_object = Mapping(mode)

    if mode == 1:
        names = Building.objects.values_list('name', flat=True)
        latitudes = Building.objects.values_list('latitude', flat=True)
        longitudes = Building.objects.values_list('longitude', flat=True)
        colors = Building.objects.values_list('color', flat=True)
        roles = Building.objects.values_list('role', flat=True)
        prefixs = Building.objects.values_list('prefix', flat=True)
        homepages = Building.objects.values_list('homepage', flat=True)
        map_object.Basicing(names, latitudes, longitudes, colors, roles, prefixs, homepages)
    if mode == 2:
        walk_count = Search.objects.count()
        departure = Search.objects.get(id=walk_count).departure
        arrival = Search.objects.get(id=walk_count).arrival
        if departure != arrival:
            map_object.Searching(departure, arrival)
        else:
            messages.add_message(request, messages.ERROR, "출발지와 목적지가 같습니다")
            return HttpResponseRedirect(reverse('mapapp:search'))
    if mode == 3:
        bus_count = Search_Bus.objects.count()
        map_object.Bus(bus_count)

    chosunmap = map_object.getmap()
    plugins.LocateControl().add_to(chosunmap)
    plugins.Geocoder().add_to(chosunmap)
    maps = chosunmap._repr_html_()  # 지도를 템플릿에 삽입하기위해 iframe이 있는 문자열로 반환 (folium)

    return render(request, 'mapapp/map.html', {'map': maps})


# def Search(request):
#     return render(request,'mapapp/search.html')

class SearchCreateView(CreateView):
    model = Search
    form_class = SearchCreationForm
    # success_url = reverse_lazy('mapapp:map')
    template_name = 'mapapp/search.html'

    def get_success_url(self):
        mo = Mode.objects.get(id=1)
        mo.mode = 2  # map mode = 2 Search
        mo.save()
        return reverse('mapapp:map')


class BusCreativeView(CreateView):
    model = Search_Bus
    form_class = BusCreationForm
    template_name = 'mapapp/bus.html'

    def get_success_url(self):
        mo = Mode.objects.get(id=1)
        mo.mode = 3  # map mode = 3 Bus route
        mo.save()
        return reverse('mapapp:map')

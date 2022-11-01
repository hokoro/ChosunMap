import folium
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView
from folium import plugins

# Create your views here.
from mapapp.forms import SearchCreationForm
from mapapp.map import Mapping
from mapapp.models import Building, Search, Mode


def SetMap(request):
    mode = Mode.objects.get(id=1).mode
    names = Building.objects.values_list('name', flat=True)
    latitudes = Building.objects.values_list('latitude', flat=True)
    longitudes = Building.objects.values_list('longitude', flat=True)
    colors = Building.objects.values_list('color', flat=True)
    mappings = Building.objects.values_list('mapping', flat=True)
    roles = Building.objects.values_list('role', flat=True)
    prefixs = Building.objects.values_list('prefix', flat=True)
    homepages = Building.objects.values_list('hompage', flat=True)

    map_object = Mapping(names, latitudes, longitudes, colors, mappings, roles, prefixs, homepages)

    if mode:
        map_object.Basicing()
    else:
        map_object.Searching()

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
        mo.mode = False
        mo.save()
        return reverse('mapapp:map')

import folium

from mapapp.models import Mode, Search, Building


class Mapping:
    def __init__(self, name, latitude, longitude, color, mapping, role, prefix, homepage):
        self.map_mode = Mode.objects.get(id=1).mode
        self.names = name
        self.latitudes = latitude
        self.longitudes = longitude
        self.colors = color
        self.mappings = mapping
        self.roles = role
        self.prefixes = prefix
        self.homepages = homepage
        self.map = folium.Map(location=[35.14084745080004, 126.93006806955218], zoom_start=17,
                              width='100%', height='100%')
        self.count = Search.objects.count()
        self.search = Search.objects.get(id=self.count)

    def Basicing(self):
        print('기본 모드')
        for name, latitude, longitude, color, mapping, role, prefix, homepage in zip(self.names, self.latitudes,
                                                                                     self.longitudes, self.colors,
                                                                                     self.mappings, self.roles,
                                                                                     self.prefixes, self.homepages):
            if mapping:
                if prefix:
                    folium.Marker(
                        location=[latitude, longitude],
                        icon=folium.Icon(color=color, icon=role, prefix='fa'),
                        popup=f"<a href={homepage} target=_blank><pre>{name}</pre></a>",
                        tooltip=name,
                    ).add_to(self.map)
                else:
                    folium.Marker(
                        location=[latitude, longitude],
                        icon=folium.Icon(color=color, icon=role),
                        popup=f"<a href={homepage} target=_blank><pre>{name}</pre></a>",
                        tooltip=name,
                    ).add_to(self.map)
            else:
                continue

    def Searching(self):
        print('검색 모드')
        departure = self.search.departure
        arrival = self.search.arrival

        print(departure, arrival)

        dep = Building.objects.get(name=departure)
        arr = Building.objects.get(name=arrival)

        print(dep.name, arr.name)

        search_list = [dep, arr]

        for search in search_list:
            if search.prefix:
                folium.Marker(
                    location=[search.latitude, search.longitude],
                    icon=folium.Icon(color=search.color, icon=search.role, prefix='fa'),
                    popup=f"<a href={search.hompage} target=_blank><pre>{search.name}</pre></a>",
                    tooltip=search.name,
                ).add_to(self.map)
            else:
                folium.Marker(
                    location=[search.latitude, search.longitude],
                    icon=folium.Icon(color=search.color, icon=search.role),
                    popup=f"<a href={search.hompage} target=_blank><pre>{search.name}</pre></a>",
                    tooltip=search.name,
                ).add_to(self.map)

        mo = Mode.objects.get(id=1)
        mo.mode = True
        mo.save()

    def getmap(self):
        return self.map

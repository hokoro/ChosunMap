import folium

from mapapp.models import Mode, Search, Building, Data, Search_Bus, Route, Bus, Node, Road
import pandas as pd
import numpy as np
from mapapp import ACO

# folium add legend label
"""
reference : https://stackoverflow.com/questions/65042654/how-to-add-categorical-legend-to-python-folium-map

function parameter
folium_map : label 을 적용 시킬 맵 
title : labels title
colors : label 하나 하나 의 색  
labels : label 의 내용
mode: 길의 안내 / 길의 경로 (Boolean) 
"""


def add_categorical_legend(folium_map, title, colors, labels, mode):
    legend_categories = ""
    if mode:  # mode == True -> color : label 버전으로 출력
        color_by_label = dict(zip(labels, colors))  # label 과 color 를 하나의 dict 으로 설정
        # add color + label list html
        for label, color in color_by_label.items():
            legend_categories += f"<li><span style='background:{color}'></span>{label}</li>"  # 목록이 있는 리스트 설정을 위해 <li> tag 를 사용
    else:  # mode == False -> label (부분 경로) 버전으로 출력
        for label in labels:
            legend_categories += f"<li>{label}</li>"  # 경로 출력이기 때문에 색깔 x label 만 추가

    # add legend label information html
    """
    maplegend : 전체 div의 틀 
    legend-title : legend 의 제목  
    legend-scale : legend 의 구조
    legend-labels : legend label 
    """
    legend_html = f"""
    <div id='maplegend' class='maplegend'>
      <div class='legend-title'>{title}</div> 
      <div class='legend-scale'>
        <ul class='legend-labels'>
        {legend_categories}
        </ul>
      </div>
    </div>
    """

    # legend_html js
    """
    label 존재 여부 / 함수 실행 여부를 통해 
    setInterval 실행 할때마다 Update 
    legend label 의 style 옵션을 변경해 주는 함수 
    display = flex -> 해당 div/container 에 맞게 크기를 조정 
    flexDirection = column -> label 을 배치 하는 방법 (column 왼쪽 -> 오른쪽으로 가는 배치)
    innerHTML += {legend_html} -> 아까 재작한 html 을 추가 (label 작성 )
    """

    script = f""" 
    <script type="text/javascript"> 
    var oneTimeExecution = ( function() 
        {{ 
            var executed = false; 
            return function() 
            {{ 
                if (!executed) 
                    {{ var checkExist = setInterval(function() 
                        {{ if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed))  
                            {{ 
                                document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex" 
                                document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column" 
                                document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`; 
                                clearInterval(checkExist);
                                executed = true;
                            }}
                        }}, 100);
                    }}
            }};
        }})();
        oneTimeExecution()
        </script>
      """

    # legend html css
    """
    각각의 div 요소에 대한 css 옵션 값 
    z-index : 요소 수직 정령
    float : 요소 정렬 
    """

    css = """
    <style type='text/css'>
      .maplegend {
        z-index:9999;
        float:right;
        background-color: rgba(255, 255, 255, 1);
        border-radius: 5px;
        border: 2px solid #bbb;
        padding: 10px;
        font-size:12px;
        positon: relative;
      }
      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 0px solid #ccc;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }
    </style>
    """

    folium_map.get_root().header.add_child(folium.Element(script + css))


class Mapping:
    def __init__(self, mode):
        self.map_mode = mode
        self.map = folium.Map(location=[35.14084745080004, 126.93006806955218], zoom_start=17,
                              width='100%', height='100%')

    def Basicing(self, names, latitudes, longitudes, colors, roles, prefixs, homepages):
        for name, latitude, longitude, color, role, prefix, homepage in zip(names, latitudes,
                                                                            longitudes, colors,
                                                                            roles, prefixs,
                                                                            homepages):

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

    # ACO BEST ROUTE PATH
    def Searching(self, departure, arrival):
        # start = departure index , end = arrival index
        start = Node.objects.get(name=departure).number
        end = Node.objects.get(name=arrival).number

        # Data Frame convert to 2d array graph
        distance_df = pd.read_csv(Data.objects.get(name='distance').data, encoding='utf-8-sig').iloc[0:,
                      2:]
        time_df = pd.read_csv(Data.objects.get(name='time').data, encoding='utf-8-sig').iloc[0:, 3:]

        # Nan = np.inf
        distance_df = distance_df.fillna(np.inf)
        time_df = time_df.fillna(np.inf)

        # df convert nd array
        dis_np = distance_df.to_numpy()
        time_np = time_df.to_numpy()

        # ACO object
        distance_aco = ACO.AntColony(start, end, dis_np, 10, 1, 300, 0.95, alpha=1.2, beta=1.0)
        time_aco = ACO.AntColony(start, end, time_np, 10, 1, 300, 0.95, alpha=1.2, beta=1.0)
        # ACO Run()
        distance_path = distance_aco.run()
        time_path = time_aco.run()

        # distance_list , time_list latitude , longitude
        distance_lal = []
        time_lal = []

        # distance_list / time_list -> 부분 (거리/시간) / 총 (거리/시간) 합을 구하기 위함
        distance_list = []
        time_list = []

        # distance_node_name / time_node_name -> Node name compare with distance and time
        distance_node_list = []
        time_node_list = []
        # distance route str
        distance_str = []
        time_str = []
        for i in range(len(distance_path[0]) - 1):
            distance_list.append(dis_np[distance_path[0][i]][distance_path[0][i + 1]])  # numpy 에 있는 A->B 가는 거리
            distance_node_list.append(          # A->B 가는 경로의 이름
                [Node.objects.get(number=distance_path[0][i]).name,
                 Node.objects.get(number=distance_path[0][i + 1]).name])
            distance_str.append(    # A->B 가는 경로 를 문자열로 저장
                f' {i + 1} 경로 : {distance_node_list[i][0]} -- > {distance_node_list[i][1]} 거리: {distance_list[i]}m \n')
        # time sum
        for i in range(len(time_path[0]) - 1):
            time_list.append(int(time_np[time_path[0][i]][time_path[0][i + 1]]))    # numpy 에 있는 A->B 가는 시간
            time_node_list.append(      # A->B 가는 경로의 이름
                [Node.objects.get(number=time_path[0][i]).name, Node.objects.get(number=time_path[0][i + 1]).name])
            time_str.append(    # A->B 가는 경로 를 문자열로 저장
                f' {i + 1} 경로 : {time_node_list[i][0]} -- > {time_node_list[i][1]} 거리: {time_list[i] // 60}분 {time_list[i] % 60}초 \n')
        # distance path convert Building or Road
        for distance in distance_path[0]:
            distance_location = Node.objects.get(number=distance).name  # Node 들의 이름을 DB 에서 반환

            # distance over 54 = Road information
            if distance > 53:
                road_data = Road.objects.get(name=distance_location)            # 도로 DB 에 해당되는 행 데이터 반환
                distance_lal.append([road_data.latitude, road_data.longitude])  # list append latitude and longitude
            # distance under 54 = Building information
            else:
                building_data = Building.objects.get(name=distance_location)     # 건물 DB 에 해당되는 행 데이터 반환
                distance_lal.append([building_data.latitude, building_data.longitude])  # list append latitude and longitude

                # Building information add Folium marker
                if building_data.prefix:
                    folium.Marker(
                        location=[building_data.latitude, building_data.longitude],
                        icon=folium.Icon(color=building_data.color, icon=building_data.role, prefix='fa'),
                        popup=f"<a href={building_data.homepage} target=_blank><pre>{building_data.name}</pre></a>",
                        tooltip=building_data.name,
                    ).add_to(self.map)
                else:
                    folium.Marker(
                        location=[building_data.latitude, building_data.longitude],
                        icon=folium.Icon(color=building_data.color, icon=building_data.role),
                        popup=f"<a href={building_data.homepage} target=_blank><pre>{building_data.name}</pre></a>",
                        tooltip=building_data.name,
                    ).add_to(self.map)
        # time path convert Building or Road
        for time in time_path[0]:
            time_location = Node.objects.get(number=time).name

            # time over 54 = Road information
            if time > 53:
                road_data = Road.objects.get(name=time_location)    # 도로 DB 에 해당되는 행 데이터 반환
                time_lal.append([road_data.latitude, road_data.longitude])  # list append latitude and longitude
            # time under 54 = Building information
            else:
                building_data = Building.objects.get(name=time_location)    # 건물 DB 에 해당되는 행 데이터 반환
                time_lal.append([building_data.latitude, building_data.longitude])  # list append latitude and longitude

                # external ICON = Prefix True
                if building_data.prefix:
                    folium.Marker(
                        location=[building_data.latitude, building_data.longitude],
                        icon=folium.Icon(color=building_data.color, icon=building_data.role, prefix='fa'),
                        popup=f"<a href={building_data.homepage} target=_blank><pre>{building_data.name}</pre></a>",
                        tooltip=building_data.name,
                    ).add_to(self.map)
                # Internal ICON = Prefix False
                else:
                    folium.Marker(
                        location=[building_data.latitude, building_data.longitude],
                        icon=folium.Icon(color=building_data.color, icon=building_data.role),
                        popup=f"<a href={building_data.homepage} target=_blank><pre>{building_data.name}</pre></a>",
                        tooltip=building_data.name,
                    ).add_to(self.map)

        # poly line case 1.distance route 2.time route
        if distance_node_list == time_node_list:     # 최단 거리 경로 == 최단 시간 경로
            folium.PolyLine(locations=distance_lal, color='green').add_to(self.map)
        else:
            folium.PolyLine(locations=distance_lal, color='red').add_to(self.map)
            folium.PolyLine(locations=time_lal, color='blue').add_to(self.map)

        # Route legend label
        add_categorical_legend(self.map, title="경로 정보", colors=["red", "blue", "green"],
                               labels=["거리 최적", "시간 최적", "거리/시간 동일"], mode=True)
        add_categorical_legend(self.map, title="거리/시간", colors=["red", "blue"],
                               labels=[f'{sum(distance_list)}m', f'{sum(time_list) // 60}분 {sum(time_list) % 60}초'],
                               mode=True)
        add_categorical_legend(self.map, title="거리 경로", colors=["red"], labels=[distance for distance in distance_str],
                               mode=False)
        add_categorical_legend(self.map, title="시간 경로", colors=["blue"], labels=[time for time in time_str],
                               mode=False)

    # Bus Route information Function
    def Bus(self, bus_count):
        destination = Search_Bus.objects.get(id=bus_count).route
        route = Route.objects.get(name=destination)
        route_list = list(route.route.split('-'))
        location_data = []
        bus_station_str = ""
        # Bus Station Icon
        for r in route_list:
            latitude = Bus.objects.get(name=r).latitude
            longitude = Bus.objects.get(name=r).longitude
            location_data.append([latitude, longitude])

            if Bus.objects.get(name=r).id < 14:
                bus_station_str += f'{r}-'
                folium.Marker(
                    location=[latitude, longitude],
                    icon=folium.Icon(color='blue', icon='info-sign'),
                    popup=f"<a href><pre>{r}</pre></a>",
                    tooltip=r,
                ).add_to(self.map)
            else:
                continue

        # Bus Polyline
        color = ''
        if destination == '본관행':
            color = 'blue'

        if destination == '사회과학관행':
            color = 'red'

        if destination == '글로벌하우스행':
            color = 'green'

        # Bus PolyLine
        folium.PolyLine(locations=location_data, tooltip='Polyline', color=color).add_to(self.map)

        # Bus legend label
        add_categorical_legend(self.map, "버스 노선", colors=["blue", "red", "green"],
                               labels=["본관행", "사회과학관행", "글로벌하우스행"], mode=True)
        add_categorical_legend(self.map, "정류장 이름", colors=[color], labels=[bus_station_str[:-1]], mode=True)

    def getmap(self):
        return self.map

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ChosunMap.settings")

import django

django.setup()

from mapapp.models import Node, Road, Building, Bus, Data
import pandas as pd
import numpy as np

# distance_df = pd.read_csv(Data.objects.get(name='distance').data, encoding='utf-8-sig').iloc[0:, 2:]
# time_df = pd.read_csv(Data.objects.get(name='time').data, encoding='utf-8-sig').iloc[0:, 2:]
#
# distance_df = distance_df.fillna(np.inf)
# time_df = time_df.fillna(np.inf)
# # print(distance_df)
# # print(time_df)
#
# dis_np = distance_df.to_numpy()
# time_np = time_df.to_numpy()
#
# dis_arr = dis_np.tolist()
# time_arr = time_np.tolist()
#
# print(type(dis_arr))
# print(type(dis_arr[0]))
# print(type(dis_arr[0][0]))

# print(time_arr)


building_df = pd.read_csv(Data.objects.get(name='building').data, encoding='utf-8-sig')
node_df = pd.read_csv(Data.objects.get(name='node').data, encoding='utf-8-sig')
road_df = pd.read_csv(Data.objects.get(name='road').data, encoding='utf-8-sig')
bus_df = pd.read_csv(Data.objects.get(name='bus').data, encoding='utf-8-sig')

for i in range(building_df.index.stop):
    print(building_df['name'][i])
    print(building_df['latitude'][i])
    print(building_df['longitude'][i])
    print(building_df['color'][i])
    print(building_df['role'][i])
    print(building_df['hompage'][i])

    Building.objects.create(name=building_df['name'][i], latitude=building_df['latitude'][i],
                            longitude=building_df['longitude'][i], color=building_df['color'][i],
                            role=building_df['role'][i], homepage=building_df['hompage'][i],
                            prefix=building_df['prefix'][i])

for i in range(node_df.index.stop):
    print(node_df['name'][i])
    print(node_df['index'][i])
    Node.objects.create(name=node_df['name'][i], number=node_df['index'][i])

for i in range(road_df.index.stop):
    print(road_df['location'][i])
    print(road_df['latitude'][i])
    print(road_df['longitude'][i])
    Road.objects.create(name=road_df['location'][i], latitude=road_df['latitude'][i], longitude=road_df['longitude'][i])

for i in range(bus_df.index.stop):
    print(bus_df['location'][i])
    print(bus_df['latitude'][i])
    print(bus_df['longitude'][i])
    Bus.objects.create(name=bus_df['location'][i], latitude=bus_df['latitude'][i], longitude=bus_df['longitude'][i])

# ChosunMap
## 1.기획의도 
- 조선대학교 신입생 혹인 조선대 를 처음 방문하시는 분들을 위한 길찾기 프로그램 
- 기존의 길찾기 프로그램과 차별점은 도로 를 중심으로 도보 길찾기 를 하는 방식 
- 도보형 데이터를 직접 데이터 화 하여 제작 
- 인공지능 알고리즘인 개미 군집화 알고리즘을 사용한 반응형 레이아웃 웹페이지 를 제작 

## 2.데이터 
담당자 : 이상훈 , 김장섭 , 강서진 
### 1.Building
<img src="https://github.com/hokoro/ChosunMap/blob/master/media/Image/Building.png" width="50%" height="50%">

|Column|설명|
|------|---|
|name|건물의 이름|
|latitude|건물의 위도|
|longitude|건물의 경도|
|color|건물의 색깔|
|role|건물 아이콘의 모양|
|homepage|학과 홈페이지 주소|
|prefix|외부 아이콘 결정 여부|

- folium 에서 Marker 함수를 사용하여 찍을 데이터 셋 
- prefix 는 folium 에서 기본 제공하는 아이콘이 아닐떄 사용하는 옵션 



### 2.Road
<img src="https://github.com/hokoro/ChosunMap/blob/master/media/Image/Road.png" width="50%" height="50%">

|Column|설명|
|------|---|
|name|도로의 이름|
|latitude|건물의 위도|
|longitude|건물의 경도|

- 최적 루트를 연결하기 위한 도로 포인트 데이터 셋 

### 3.Node
<img src="https://github.com/hokoro/ChosunMap/blob/master/media/Image/Road.png" width="50%" height="50%">

|Column|설명|
|------|---|
|name|건물 + 도로 의 정보|
|number|그래프 인덱스 정보|

- 그래프 에서 사용할 건물 + 도로 노드의 정보 
- number = 그래프 index 

### 4.Bus
<img src="https://github.com/hokoro/ChosunMap/blob/master/media/Image/Node.png" width="50%" height="50%">

|Column|설명|
|------|---|
|name|버스 정류장/도로 의 정보|
|latitude|각 위치의 위도|
|longitude|각 위치의 경도|


### 5.Distance
<img src="https://github.com/hokoro/ChosunMap/blob/master/media/Image/distance.jpg" width="50%" height="50%">

- 노드와 노드 사이의 거리를 나타내는 데이터

### 6.Time 
<img src="https://github.com/hokoro/ChosunMap/blob/master/media/Image/time.jpg" width="50%" height="50%">

- 노드와 노드 사이의 걸리는 시간을 나타내는 데이터  

## 3.ACO
담당자 : 이경근

- 유전 알고리즘 중 하나인 개미 알고리즘 을 통한 최적 경로 계산 
- 거리/시간 그래프 두개를 토대로 두가지의 결과를 도출 

### 개미 알고리즘의 개념 
[알고리즘](http://antalg.egloos.com/v/82254)
- 집을 막 나온 개미들은 무작정 개미집 주변을 돌아다닌다.
- 만약 음식을 찾아내면 개미는 페로몬을 뿌리며 집으로 돌아온다.
- 이후에 집을 나오는 개미들은 페로몬을 따라 이동할 확률이 높다.
- 개미가 집으로 돌아오는 횟수가 많을수록 그 경로는 더 견고해진다.
- 긴 경로와 짧은 경로가 있으면 같은 시간에 짧은 경로로 이동할 수 있는 횟수가 많다.
- 짧은 경로는 갈수록 더 많은 페로몬이 뿌려지면서 더욱 견고해진다.
- 페로몬은 휘발성이기 때문에 시간이 지나면서 긴 경로는 사라진다.
- 결국 모든 개미가 짧은 경로를 선택한다.
 
### 개미 알고리즘 참고 소스
[소스](https://github.com/Akavall/AntColonyOptimization/blob/c585c5cfc9b0e6b709322ac15fe1e2193b20d8e4/ant_colony.py#L44)

#### 기존 알고리즘과의 차이점
- 모든 노드가 연결되어 있지 않아도 실행할 수 있도록 변경
```python
realvisited = list()
realvisited.append(start)

if move == False:
  realvisited.remove(prev)
  prev = realvisited[len(realvisited)-1]
  path.pop()
else:
  path.append((prev, move))
  prev = move
  visited.append(move)
  realvisited.append((move))
  if prev == goal:
    break
```

- 목적지와 인접한 노드의 페로몬 값을 미리 증가시켜 탐색시간 감소
```python
for i in range(len(self.distances[0])):
  if self.pheromone[(self.goal, i)] and self.pheromone[(i, self.goal)] != 0:
    self.pheromone[(self.goal, i)] += 2
    self.pheromone[(i, self.goal)] += 2
```
### 향상된 개미 알고리즘 참고 논문 
[논문](https://www.hindawi.com/journals/mpe/2016/7672839/)

## 4.Web
담당자 : 천영성 

언어 : Python , HTML , CSS 

백엔드 : Django 

DB : sqlite3

- 도보형 그래프 와 ACO 알고리즘 을 적용한 결과를 시각화 하여 보여줄 반응형 레이아웃 웹 페이지 

### 기본 지도 

- Folium Marker 를 사용한 조선대학교 건물 에 대한 정보를 알려주는 기본지도 

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/ywwJvJAwo2s/maxresdefault.jpg)](https://www.youtube.com/watch?v=ywwJvJAwo2s)

### 검색 지도 

- Folium Marker , Polyline , label 을 사용하여 건물 과 건물 사이의 거리/시간 기반 최적 경로를 알려주는 기능 

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/KZebt58eN68/maxresdefault.jpg)](https://www.youtube.com/watch?v=KZebt58eN68)

### 버스 지도 

- Folium Marker , Polyline , label 을 사용하여 조선대학교 교내 버스 루트 를 알려주는 기능 
  

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/a4NY-l7IhHs/maxresdefault.jpg)](https://www.youtube.com/watch?v=a4NY-l7IhHs)



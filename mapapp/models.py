from django.db import models


# Create your models here.

class Mode(models.Model):
    mode = models.IntegerField(null=False, blank=False)


class Data(models.Model):
    name = models.CharField(max_length=15, blank=False, null=False)
    data = models.FileField(upload_to='data/', null=False)


class Node(models.Model):
    name = models.CharField(max_length=30)
    number = models.IntegerField(blank=False)


class Bus(models.Model):
    name = models.CharField(max_length=30)
    latitude = models.FloatField(null=False, blank=False)
    longitude = models.FloatField(null=False, blank=False)


class Route(models.Model):
    name = models.CharField(max_length=10)
    route = models.CharField(max_length=400)


class Road(models.Model):
    name = models.CharField(max_length=30)
    latitude = models.FloatField(null=False, blank=False)
    longitude = models.FloatField(null=False, blank=False)


class Building(models.Model):
    name = models.CharField(max_length=30)
    latitude = models.FloatField(null=False, blank=False)
    longitude = models.FloatField(null=False, blank=False)
    color = models.CharField(max_length=10, null=True)
    role = models.CharField(max_length=10, null=True)
    homepage = models.CharField(max_length=100, null=True, blank=False)
    prefix = models.BooleanField(default=False)


class Search_Bus(models.Model):
    bus_route = (
        ('본관행', '본관행'),
        ('사회과학관행', '사회과학관행'),
        ('글로벌하우스행', '글로벌하우스행')
    )

    route = models.CharField(max_length=20, choices=bus_route)


class Search(models.Model):
    buildings = (
        ('1.8극장(노천극장)', '1.8극장(노천극장)'),
        ('IT융합대학', 'IT융합대학'),
        ('경상대학', '경상대학'),
        ('공과대학제1공학관', '공과대학제1공학관'),
        ('공과대학제2공학관', '공과대학제2공학관'),
        ('교수연구동', '교수연구동'),
        ('국제관(언어교육원)', '국제관(언어교육원)'),
        ('그린빌리지(기숙사)', '그린빌리지(기숙사)'),
        ('글로벌하우스(기숙사)', '글로벌하우스(기숙사)'),
        ('대운동장', '대운동장'),
        ('미술대학(미술관)', '미술대학(미술관)'),
        ('백학여학사(기숙사)', '백학여학사(기숙사)'),
        ('법과대학', '법과대학'),
        ('본관', '본관'),
        ('사회대학&사범대학', '사회대학&사범대학'),
        ('생명공학관', '생명공학관'),
        ('생산교육실험실습동', '생산교육실험실습동'),
        ('서석홀', '서석홀'),
        ('백학남학사(기숙사)', '백학남학사(기숙사)'),
        ('솔마루(식당)', '솔마루(식당)'),
        ('약학대학1호관(약학관)', '약학대학1호관(약학관)'),
        ('약학대학2호관', '약학대학2호관'),
        ('약학대학3호관(강의동)', '약학대학3호관(강의동)'),
        ('의과대학1호관', '의과대학1호관'),
        ('의과대학2호관', '의과대학2호관'),
        ('의과대학3호관', '의과대학3호관'),
        ('의성관(연구동)', '의성관(연구동)'),
        ('입석홀(식당)', '입석홀(식당)'),
        ('자연과학관', '자연과학관'),
        ('장미원', '장미원'),
        ('장황남정보통신박물관', '장황남정보통신박물관'),
        ('조선대간호대학', '조선대간호대학'),
        ('조선대학교병원', '조선대학교병원'),
        ('조선대학교부속고등학교', '조선대학교부속고등학교'),
        ('조선대학교부속중학교', '조선대학교부속중학교'),
        ('조선대학교어린이집', '조선대학교어린이집'),
        ('조선대학교여자고등학교', '조선대학교여자고등학교'),
        ('조선대학교여자중학교', '조선대학교여자중학교'),
        ('조선대학교치과병원', '조선대학교치과병원'),
        ('조선대학교병원장례식장', '조선대학교병원장례식장'),
        ('조선이공대1공학관&3공학관', '조선이공대1공학관&3공학관'),
        ('조선이공대2공학관&4공학관', '조선이공대2공학관&4공학관'),
        ('주차빌딩', '주차빌딩'),
        ('중앙도서관', '중앙도서관'),
        ('창업보육센터', '창업보육센터'),
        ('체육대학', '체육대학'),
        ('치과대학(교육동)', '치과대학(교육동)'),
        ('치과대학(연구동)', '치과대학(연구동)'),
        ('태양에너지실증연구단지', '태양에너지실증연구단지'),
        ('학군단(ROTC)', '학군단(ROTC)'),
        ('학생회관(동아리연합회)', '학생회관(동아리연합회)'),
        ('항공우주&선박해양공학관', '항공우주&선박해양공학관'),
        ('해오름관', '해오름관'),
        ('황금추관(고시원)', '황금추관(고시원)'),

    )
    departure = models.CharField(max_length=40, choices=buildings)
    arrival = models.CharField(max_length=40, choices=buildings)

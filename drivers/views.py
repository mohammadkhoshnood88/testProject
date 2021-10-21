from django.shortcuts import render
from django.http import HttpResponse
from django.middleware import csrf
from django.db.models import Q , QuerySet
from django.views.decorators.csrf import csrf_exempt
import json
from . import models
import logging
from django.contrib.gis.geos import GEOSGeometry , Point , Polygon , MultiLineString , LineString

logger = logging.getLogger('tests')


def index(request,id):
    return HttpResponse(id)

def read_json(request ,):

    # with open('C:/Users/HepahhangRayaneh/Django/First/Ofogh/owners.json', 'r') as f:
    #     roads = json.load(f)
    
    # a = []
    # for ind , d in enumerate(roads):
    #     new_d = models.Driver(name = roads[ind]['name'] , ncode = roads[ind]['national_code'] , age = roads[ind]['age'] , total_toll_paid = roads[ind]['total_toll_paid'])
    #     new_d.save()
    #     for indd , car in enumerate(roads[ind]['ownerCar']):
    #         new_c = models.Car(driver = new_d , color = car['color'] , length = car['length'] , load_valume = car['load_valume'] , ctype = ("s" if car['type'] == "small" else 'b'))
    #         new_c.save()
    
    # drivers = models.Driver.objects.all()
    # return HttpResponse(drivers)

    # with open('C:/Users/HepahhangRayaneh/Django/First/Ofogh/nodes.json', 'r') as f:
    #     nodes = json.load(f)

    # for ind , d in enumerate(nodes):
    #     car = models.Car.objects.get(id = nodes[ind]['car'])

    #     node = nodes[ind]['location'].split(';')[1]
    #     a = GEOSGeometry(node)
    #     point = Point(a[0] , a[1])
        
    #     new_node = models.Node(location = point , car = car , date = nodes[ind]['date'])
    #     new_node.save()
    
    # nodes = models.Node.objects.all()
    # return HttpResponse(nodes)    

    # with open('C:/Users/HepahhangRayaneh/Django/First/Ofogh/roads.json', 'r') as f:
    #     roads = json.load(f)

    # road = roads[0]['geom'].split(';')[1]
    # a = GEOSGeometry(road)
    # point = MultiLineString(a)

    # new_road = models.Road(geom = a , name = roads[0]['name'] ,  width = roads[0]['width'])
    # new_road.save()

    # return HttpResponse(new_road)
    
    # for ind , d in enumerate(roads):
        
    #     road = roads[ind]['geom'].split(';')[1]
    #     a = GEOSGeometry(road)
        
    #     new_road = models.Road(geom = a , name = roads[ind]['name'] ,  width = roads[ind]['width'])
    #     new_road.save()
    
    # roads = models.Road.objects.all()

    # return HttpResponse(roads)


    with open('C:/Users/HepahhangRayaneh/Django/First/Ofogh/tollstation.json', 'r') as f:
        stations = json.load(f)
    
    for ind , d in enumerate(stations):
        
        station = stations[ind]['location'].split(';')[1]
        a = GEOSGeometry(station)
        point = Point(a[0] , a[1])
        
        new_station = models.TollStation(location = point , name = stations[ind]['name'] ,  toll_per_cross = stations[ind]['toll_per_cross'])
        new_station.save()
    
    stations = models.TollStation.objects.all()

    return HttpResponse(stations)


@csrf_exempt
def cars(request , ):
    
    body_unicode = request.body.decode('utf-8')
    colors = json.loads(body_unicode)['colors']
    
    query = Q()
    for color in colors:
        query |= Q(color = color)

    cars = models.Car.objects.filter(query)
    return HttpResponse(cars)


@csrf_exempt
def store_car(request ,id):
    driver = models.Driver.objects.get(id = id)

    body_unicode = request.body.decode('utf-8')
    car = json.loads(body_unicode)    

    new_c = models.Car(driver = driver , color = car['color'] , length = car['length'] , ctype = ("s" if car['type'] == 0 else 'b'))
    new_c.save()

    return HttpResponse("new car added")


##################################### drivers ####################################


@csrf_exempt
def drivers(request):
    drivers = models.Driver.objects.filter(age__gt = 70)
    ids = [driver.id for driver in drivers]
    related_cars = models.Car.objects.filter(driver__in = ids)
    return HttpResponse(related_cars)


@csrf_exempt
def store_driver(request):
    
    body_unicode = request.body.decode('utf-8')
    req = json.loads(body_unicode)

    new_d = models.Driver(name = req['name'] , ncode = req['national_code'] , age = req['age'])
    new_d.save()
    for indd , car in enumerate(req['cars']):
        models.Car.check(new_d)
        new_c = models.Car(driver = new_d , color = car['color'] , length = car['length'] , ctype = ("s" if car['type'] == 0 else 'b'))
        new_c.save()

    return HttpResponse("new user added")



@csrf_exempt
def driver(request):
    return HttpResponse("drivers")

#############################  nodes   #############################

@csrf_exempt
def allowed_traffic(request):

    node = models.Node.objects.get(id = 10)

    point = Point(node.location[0], node.location[1], srid=4326)

    node2 = models.Node.objects.get(id = 12)

    point2 = Point(node2.location[0], node2.location[1], srid=4326)

    roads = models.Road.objects.filter(width__lte = 20)

    nodes = models.Node.objects.all()
    
    big_cars = []
    for node in nodes:
        if node.car.ctype == 'b':
            big_cars.append(node)
    
    dont_allowed_car = []
    for car in big_cars:
        point = Point(car.location[0], car.location[1], srid=4326)
        for road in roads:
            mls = MultiLineString(road.geom[0])
            prep_poly = mls.prepared
            if prep_poly.contains(point):
                dont_allowed_car.append((road.name ))

    return HttpResponse(dont_allowed_car)



@csrf_exempt
def near_tollstation(request):
    station = models.TollStation.objects.get(id = 4)

    point = Point(station.location[0], station.location[1], srid=4326)

    nodes = models.Node.objects.all()
    all_near_nodes = []
    for node in nodes:
        node_point = Point(node.location[0], node.location[1], srid=4326)
        if point.distance(node_point) * 100000 < 600:
            all_near_nodes.append(node)

    near_nodes = []
    for node in all_near_nodes:
        if node.car.ctype == 's':
            near_nodes.append(node)


    return HttpResponse(near_nodes)


def tollstation_in_road(request):
    
    stations = models.TollStation.objects.all()
    roads = models.Road.objects.all()

    # result = models.Node.objects.values('car')

    result = (models.Node.objects
        .values('car_id' , 'location')
        .order_by()
    )
    group = {}

    for node in models.Node.objects.all():
        temp = []
        if node.car_id in group:
            group[node.car_id].append(node)
        else:
            temp.append(node)
            group[node.car_id] = temp
        

    for gp in group[1]:
        for gpp in group[1]:
            LineString([Point(gp.location[0] , gp.location[1]) , Point(gpp.location[0] , gpp.location[1])]).wkt
        

    return HttpResponse(group[1])
from django.urls import path
from django.conf.urls import include, url
from . import views

app_name = 'drivers'
urlpatterns = [

    #read files
    path('read/json/', views.read_json),

    #cars
    url('cars' , views.cars),
    path('driver/<int:id>/car/store/' , views.store_car),
    
    # drivers urls
    path('drivers' , views.drivers),
    path('drivers/<int:id>' , views.driver),
    path('driver/store/' , views.store_driver),

    path('allowed-traffic/' , views.allowed_traffic),
    path('near-station/' , views.near_tollstation),
    path('test/' , views.tollstation_in_road),

]

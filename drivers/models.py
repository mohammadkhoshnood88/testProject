# from django.db import models
# from django.contrib.gis.db import models as gisModel
from django.contrib.gis.db import models

# راننده ها
class Driver(models.Model):
    name = models.CharField(max_length=30)
    ncode = models.CharField(max_length=10)
    age = models.IntegerField(default=20)
    total_toll_paid = models.FloatField(null=True , blank= True)
    
    # def __str__(self):
    #     return str(self.id)

# ماشین ها
class Car(models.Model):

    @classmethod
    def check(cls, d):
        cars = models.Node.objects.get(driver = d)
        return book


    CTYPE = (
    ('s', 'small'),
    ('b', 'big'),
    )

    driver = models.ForeignKey(Driver , on_delete=models.CASCADE)
    color = models.CharField(max_length=8)
    length = models.FloatField(null=True , blank=True)
    ctype = models.CharField(max_length=1, choices=CTYPE)
    load_valume = models.FloatField(null=True , blank=True)

    def __str__(self):
        return 'name : ' + self.driver.name + ' ---- car type : ' + (" small " if self.ctype == 's' else " big ") + ' ---- color : ' + self.color + ' |||||| '


# عوارضی
class TollStation(models.Model):
    name = models.CharField(max_length=30)
    toll_per_cross = models.IntegerField(default=1000) # مقدار عوارض ثابت هر ایستگاه
    location = models.PointField(srid=4326 , null=True)


# جاده ها
class Road(models.Model):
    
    name = models.CharField(max_length=80 , null=True , blank=True)
    width = models.FloatField()
    geom = models.MultiLineStringField(null=True)

# باری که ماشین زده
class Cargo(models.Model):
    car = models.ForeignKey(Car , on_delete=models.CASCADE)
    amount = models.IntegerField() #kg
    loaded_date = models.DateTimeField('loaded date')

# هر ماشین میاد ایستگاه پولو پرداخت میکنه
class Payment(models.Model):
    car = models.ForeignKey(Car , on_delete=models.CASCADE)
    toll_station = models.ForeignKey(TollStation , on_delete=models.CASCADE)
    amount = models.IntegerField()
    paid_date = models.DateTimeField('paid date')

class Node(models.Model):
    car = models.ForeignKey(Car , on_delete=models.CASCADE)
    location = models.PointField(srid=4326)
    date = models.DateTimeField('date' , null=True)

    # def __str__(self):
    #     return self.car.color


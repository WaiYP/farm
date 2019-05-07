from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from datetime import datetime, date

from django.db import models
from django.db import connection

class City(models.Model):
    city_name = models.CharField(max_length=250, unique=True)
    def __str__(self):
        return self.city_name
    class Meta:
        verbose_name_plural = "City List"

class Routes(models.Model):
    depart = models.ForeignKey(City, on_delete=models.SET_NULL, related_name='depart_city', null=True, blank=True)
    arrive = models.ForeignKey(City, on_delete=models.SET_NULL, related_name='arrive_city', null=True, blank=True)
    approx_hr = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    add_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return "{} - {} (Approx hr: {})".format(self.depart, self.arrive, self.approx_hr)
    class Meta:
        verbose_name_plural = "Route List"

class StopPoints(models.Model):
    route = models.ForeignKey(Routes, on_delete=models.SET_NULL, related_name='route_id', null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, related_name='city_id', null=True, blank=True)
    eta = models.CharField(max_length=100)
    def __str__(self):
        return "{} / {} / ETA: {} hr".format(self.city, self.route, self.eta)
    class Meta:
        verbose_name_plural = "Stop Points"

class BusInfo(models.Model):
    plate_num = models.CharField(max_length=100)
    host_name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=200)
    image = models.FileField(upload_to='bus_images')
    plate_photo = models.FileField(upload_to='bus_images', null=True)
    photo1 = models.FileField(upload_to='bus_images', null=True)
    photo2 = models.FileField(upload_to='bus_images', null=True)
    photo3 = models.FileField(upload_to='bus_images', null=True)
    photo4 = models.FileField(upload_to='bus_images', null=True)
    photo5 = models.FileField(upload_to='bus_images', null=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return "{} ({})".format(self.plate_num, self.type)
    class Meta:
        verbose_name_plural = "Bus List"

class Schedule(models.Model):
    bus = models.ForeignKey(BusInfo, on_delete=models.SET_NULL, null=True, blank=True)
    route = models.ForeignKey(Routes, on_delete=models.SET_NULL, null=True, blank=True)
    depart_time = models.DateTimeField(default=datetime.now, blank=True)
    arrive_time = models.DateTimeField(default=datetime.now, blank=True)
    add_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_added = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return "{} : {} @ {} {}".format(self.bus, self.route, self.arrive_time, self.arrive_time)
    class Meta:
        verbose_name_plural = "Schedule List"

    @staticmethod
    def check_schedule(busid, depart, arrive, status):
        cur = connection.cursor()
        cur.callproc('check_new_schedule', [busid, depart, arrive, status])
        results = cur.fetchall()
        cur.close()

        return results
        #return [Schedule(*row) for row in results]
        #return results.index(0)

class Seats(models.Model):
    seat_name = models.CharField(max_length=100, blank=True, null=False)
    bus = models.ForeignKey(BusInfo, on_delete=models.CASCADE, null=True, blank=True)
    seat_type = models.CharField(max_length=50, null=False)
    row_no = models.IntegerField(null=True)
    seat_no = models.IntegerField(null=True)
    price = models.IntegerField(null=True)

    def __str__(self):
        return "{} ({})".format(self.bus_id, self.seat_name)

class ExtraService(models.Model):
    eng_service_name = models.CharField(max_length=250, unique=True)
    unicode_service_name = models.CharField(max_length=250, unique=True)
    zawgyi_service_name = models.CharField(max_length=250, unique=True)
    chinese_service_name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.city_name

    class Meta:
        verbose_name_plural = "Extra Service List"

class FerryLocation(models.Model):
    location_name = models.CharField(max_length=250)
    host_name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.location_name
    class Meta:
        verbose_name_plural = "Ferry Location List"

class Role(models.Model):
    role_name = models.CharField(max_length=100, blank=True, null=True)
    active = models.NullBooleanField()
    ts = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.role_name

class BusDriver(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    unicode_name = models.CharField(max_length=250)
    zawgyi_name = models.CharField(max_length=250)
    chinese_name = models.CharField(max_length=250)
    active = models.NullBooleanField()
    ts = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name




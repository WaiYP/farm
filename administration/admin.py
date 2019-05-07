from django.contrib import admin
from .models import City, Routes, StopPoints, BusInfo, Schedule, Seats, ExtraService, FerryLocation, Role, BusDriver

admin.site.register(City)

admin.site.register(Routes)

admin.site.register(StopPoints)

class BusList(admin.ModelAdmin):
    list_display = ("plate_num", "type", "is_active", "host_name",)
    search_fields = ("plate_num", "type", "host_name",)
admin.site.register(BusInfo, BusList)

class ScheduleList(admin.ModelAdmin):
    list_display = ("bus", "route", "depart_time", "arrive_time", "add_by", "date_added",)
    search_fields = ("bus", "route", "add_by",)
    readonly_fields = ("date_added",)
admin.site.register(Schedule, ScheduleList)

admin.site.register(Seats)
admin.site.register(ExtraService)
admin.site.register(FerryLocation)
admin.site.register(Role)

class BusDriverList(admin.ModelAdmin):
    list_display = ("name", "host", "unicode_name", "chinese_name", "ts", "active",)
    search_fields = ("name", "host",)
admin.site.register(BusDriver, BusDriverList)

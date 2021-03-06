# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-06 04:32
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BusDriver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('unicode_name', models.CharField(max_length=250)),
                ('zawgyi_name', models.CharField(max_length=250)),
                ('chinese_name', models.CharField(max_length=250)),
                ('active', models.NullBooleanField()),
                ('ts', models.DateTimeField(auto_now_add=True, null=True)),
                ('host', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BusInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plate_num', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=200)),
                ('image', models.FileField(upload_to='bus_images')),
                ('is_active', models.BooleanField(default=True)),
                ('host_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Bus List',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=250, unique=True)),
            ],
            options={
                'verbose_name_plural': 'City List',
            },
        ),
        migrations.CreateModel(
            name='ExtraService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eng_service_name', models.CharField(max_length=250, unique=True)),
                ('unicode_service_name', models.CharField(max_length=250, unique=True)),
                ('zawgyi_service_name', models.CharField(max_length=250, unique=True)),
                ('chinese_service_name', models.CharField(max_length=250, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Extra Service List',
            },
        ),
        migrations.CreateModel(
            name='FerryLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=250)),
                ('host_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Ferry Location List',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(blank=True, max_length=100, null=True)),
                ('active', models.NullBooleanField()),
                ('ts', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Routes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approx_hr', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('add_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('arrive', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='arrive_city', to='administration.City')),
                ('depart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='depart_city', to='administration.City')),
            ],
            options={
                'verbose_name_plural': 'Route List',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depart_time', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('arrive_time', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('date_added', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('add_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('bus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='administration.BusInfo')),
                ('route', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='administration.Routes')),
            ],
            options={
                'verbose_name_plural': 'Schedule List',
            },
        ),
        migrations.CreateModel(
            name='Seats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_no', models.CharField(max_length=10)),
                ('seat_type', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('booked', models.BooleanField(default=False)),
                ('bus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.BusInfo')),
            ],
            options={
                'verbose_name_plural': 'Seat Plan',
            },
        ),
        migrations.CreateModel(
            name='StopPoints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eta', models.CharField(max_length=100)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='city_id', to='administration.City')),
                ('route', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='route_id', to='administration.Routes')),
            ],
            options={
                'verbose_name_plural': 'Stop Points',
            },
        ),
    ]

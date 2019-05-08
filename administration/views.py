from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from administration.forms import register_form, edit_profile_form, bus_reg_form, \
    bus_edit_form, schedule_edit_form
from django.contrib.auth.models import User
from .models import *
import os
from django.db import connection

def index(request):
    # if not request.user.is_authenticated():
    return render(request, 'administration/login.html')
    # else:
    #     return render(request, 'dashboard/index.html', {})

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'dashboard/index.html', {})
            else:
                return render(request, 'administration/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'administration/login.html', {'error_message': 'Invalid login'})
    return render(request, 'administration/login.html')

def home(request):
    if request.user.is_authenticated:
        return render(request, 'administration/admin_home.html')
    else:
        return redirect('login', permanent=True)

def change_password(request):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was updated successfully.')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'administration/user/change_password.html', {
        'form': form
    })

def register(request):
    if request.method == 'POST':
        form = register_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_register')
    else:
        form = register_form()

        reg_form = {'form': form}
        return render(request, 'administration/user/user_register.html', reg_form)

def view_profile(request):
    if request.user.is_authenticated:
        profile = {'user': request.user}
        return render(request, 'administration/user/view_profile.html', profile)
    else:
        return redirect('login', permanent=True)

def edit_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = edit_profile_form(request.POST, instance=request.user)

            if form.is_valid():
                form.save()
                return redirect('/administration/profile')
        else:
            form = edit_profile_form(instance=request.user)
            args = {'form': form}
            return render(request, 'administration/user/edit_profile.html', args)
    else:
        return redirect('login', permanent=True)

def users(request):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)
    else:
        users = User.objects.all()
        context = {
            'users': users
        }
    return render(request, 'administration/user/users.html', context)

def city(request):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    cities = City.objects.order_by('city_name')
    context = {
        'cities': cities
    }

    if request.method == 'POST':
        if request.POST.get('c_name'):
            post = City()
            post.city_name = request.POST.get('c_name')

            post.save()
            messages.success(request, 'New city added successfully.')
            return redirect('city')
        else:
            messages.error(request, 'Please complete all fields.')
            return redirect('city')
    else:
        return render(request, 'administration/city/city.html', context)

def add_city(request):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    if request.method == 'POST':
        if request.POST.get('c_name'):
            post = City()
            post.city_name = request.POST.get('c_name')
            post.save()
            messages.success(request, 'New city added successfully.')
            return redirect('city')
        else:
            messages.error(request, 'Please complete all fields.')
            return redirect('city')
    else:
        return render(request, 'administration/city/add_city.html')

def routes(request):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    routes = Routes.objects.order_by('created_at').reverse()
    return render(request, 'administration/routes/routes.html', {'routes': routes})

def add_route(request):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    if request.method == 'POST':
        new_route = Routes()
        new_route.depart_id = request.POST.get('depart')
        new_route.arrive_id = request.POST.get('arrive')
        new_route.approx_hr = request.POST.get('approx_hr')
        new_route.add_by = request.user
        new_route.save()
        messages.success(request, 'New route added to database')
        return redirect('routes')
    else:
        city = City.objects.order_by('city_name')
        return render(request, 'administration/routes/add_route.html', {'cities': city})

def edit_route(request, id):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    if request.method == "POST":
        edit_route = Routes()
        edit_route.depart_id = request.POST.get('depart')
        edit_route.arrive_id = request.POST.get('arrive')
        edit_route.approx_hr = request.POST.get('approx_hr')
        edit_route.save()
        messages.success(request, 'Route edited')
        return redirect('routes')
    else:
        route = get_object_or_404(Routes, pk=id)
        city = City.objects.order_by('city_name')
        return render(request, 'administration/routes/edit_route.html', {'route': route, 'cities': city})

def stop_points(request, id):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    if request.method == 'POST':
        new_point = StopPoints()
        new_point.route_id = id
        new_point.city_id = request.POST.get('city')
        new_point.eta = request.POST.get('approx_hr')
        new_point.save()
        return redirect('stop_points', id=id)
    else:
        route = get_object_or_404(Routes, pk=id)
        city = City.objects.order_by('city_name')
        stop_points = StopPoints.objects.filter(route_id=id)

    context = {
        'route': route,
        'cities': city,
        'stop_points': stop_points
    }
    return render(request, 'administration/routes/stop_points.html', context)

def bus_list(request):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    if request.method == 'POST':
        bus = BusInfo()
        form = bus_reg_form(request.POST, request.FILES)
        if form.is_valid():
            bus.plate_num = form.cleaned_data['plate_num']
            bus.host_name = request.user
            bus.type = form.cleaned_data['type']
            bus.image = form.cleaned_data['image']
            if not bus.image.name.lower().endswith((".jpg", ".png")):
                messages.error(request, "* Please select only JPG or PNG image!")
            else:
                bus.save()
                return redirect('bus_list')
    else:
        form = bus_reg_form()

    bus_list = BusInfo.objects.filter(host_name=request.user)
    context = {
        'bus_list': bus_list,
        'form': form
    }
    return render(request, 'administration/bus/bus.html', context)

def bus_registration(request):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    if request.method == 'POST':
        bus = BusInfo()
        form = bus_reg_form(request.POST, request.FILES)
        if form.is_valid():
            bus.plate_num = form.cleaned_data['plate_num']
            bus.host_name = request.user
            bus.type = form.cleaned_data['type']
            bus.image = form.cleaned_data['image']
            bus.plate_photo  = form.cleaned_data['plate_photo']
            bus.photo1 = form.cleaned_data['photo1']
            bus.photo2 = form.cleaned_data['photo2']
            bus.photo3 = form.cleaned_data['photo3']
            bus.photo4 = form.cleaned_data['photo4']
            bus.photo5 = form.cleaned_data['photo5']
            if not bus.image.name.lower().endswith((".jpg", ".png")):
                messages.error(request, "* Please select only JPG or PNG image!")
            else:
                bus.save()
                return redirect('bus_list')
    else:
        form = bus_reg_form()

    context = {
        'page_title': 'Register New Vehicle',
        'form': form
    }
    return render(request, 'administration/bus/bus_edit.html', context)

def bus_edit(request, id):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    instance = get_object_or_404(BusInfo, pk=id)
    if not instance.host_name == request.user:
        return redirect('bus_list')

    if request.method == 'POST':
        form = bus_edit_form(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            try:
                old_file = instance.image
            except BusInfo.DoesNotExist:
                return False

            new_file = instance.image
            if not old_file == new_file:
                if os.path.isfile(old_file.path):
                    os.remove(old_file.path)
            if not instance.image.name.lower().endswith((".jpg", ".png")):
                messages.error(request, "* Please select only JPG or PNG image!")
            else:
                form.save()
                return redirect('bus_list')
    else:
        form = bus_edit_form(instance=instance)
    context = {
        'page_title': 'Edit Vehicle - ' + instance.plate_num + ' : ' + instance.type,
        'form': form
    }
    return render(request, 'administration/bus/bus_edit.html', context)

def schedule_list(request):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    all_schedule = Schedule.objects.filter(add_by=request.user).order_by('-date_added')
    context = {
        'schedules': all_schedule
    }
    return render(request, 'administration/schedule/schedule_list.html', context)

def add_schedule(request):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    sch_bus = BusInfo.objects.filter(host_name=request.user, is_active=True)
    sch_route = Routes.objects.order_by('depart')

    context = {
        'sch_bus': sch_bus,
        'sch_route': sch_route
    }

    if request.method == 'POST':

        get_approx_hr = get_object_or_404(Routes, pk=request.POST.get('route'))

        date_ids = request.POST.getlist('checks[]')

        for day in date_ids:
            bus_depart_time = request.POST.get('d_year') + "-" + request.POST.get('d_month') + "-" + day + " " + request.POST.get('depart_time')
            for R in Routes.objects.raw("SELECT *, DATE_ADD(%s, INTERVAL %s HOUR_MINUTE) AS approx FROM administration_routes WHERE id=%s", [bus_depart_time, get_approx_hr.approx_hr, request.POST.get('route')]):
                new_sch = Schedule()
                new_sch.bus_id = request.POST.get('bus')
                new_sch.route_id = request.POST.get('route')
                new_sch.depart_time = bus_depart_time
                new_sch.arrive_time = R.approx
                new_sch.add_by = request.user
                new_sch.save()


            messages.success(request, "Schedule for " + bus_depart_time + " successfully added.")
        return redirect('add_schedule')



        #bus_depart_time = request.POST.get('depart_date') + " " + request.POST.get('depart_time')

        # for R in Routes.objects.raw("SELECT *, DATE_ADD(%s, INTERVAL %s HOUR_MINUTE) AS approx FROM administration_routes WHERE id=%s", [bus_depart_time, get_approx_hr.approx_hr, request.POST.get('route')]):
        #     new_sch = Schedule()
        #     new_sch.bus_id = request.POST.get('bus')
        #     new_sch.route_id = request.POST.get('route')
        #     new_sch.depart_time = bus_depart_time
        #     new_sch.arrive_time = R.approx
        #     new_sch.add_by = request.user
        #
        #     s_status = "0"
        #
        #     cur = connection.cursor()
        #     cur.callproc('check_new_schedule', [request.POST.get('bus'), bus_depart_time, R.approx, s_status ])
        #     #row = cur.fetchall()
            #cur.close()

            # for result in cur.stored_results():
            #     print(result.fetchall())

           #return s_status

            #results = Schedule.check_schedule(request.POST.get('bus'), bus_depart_time, R.approx, '0')


            #return HttpResponse(results[0])

            # new_sch.save()
            # messages.success(request, 'New schedule added to database')
            # return redirect('schedule_list')

    else:
        return render(request, 'administration/schedule/add_schedule.html', context)

def edit_schedule(request, id):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    schedule = get_object_or_404(Schedule, pk=id)
    if not schedule.add_by == request.user:
        return redirect('schedule_list')

    if request.method == 'POST':
        form = schedule_edit_form(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, 'Schedule edited successfully')
            return redirect('schedule_list')
    else:
        form = schedule_edit_form(instance=schedule)
    context = {
        'schedule': schedule,
        'form': form
    }

    return render(request, 'administration/schedule/edit_schedule.html', context)

def schedule_detail_popup(request, sid, rid):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    schedule = get_object_or_404(Schedule, pk=sid)
    stop_point = StopPoints.objects.filter(route_id=rid).order_by('eta')

    context = {
        'schedule': schedule,
        'stop_point': stop_point
    }
    return render(request, 'administration/popup/stop_point_popup.html', context)

def extra_service(request):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    extra_services = ExtraService.objects.order_by('id')
    context = {
        'extra_services': extra_services
    }
    return render(request, 'administration/extra_service/extra_service.html', context)

def add_extra_service(request):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    if request.method == 'POST':

            new_service = ExtraService()
            new_service.eng_service_name = request.POST.get('eng_service_name')
            new_service.unicode_service_name = request.POST.get('unicode_service_name')
            new_service.zawgyi_service_name = request.POST.get('zawgyi_service_name')
            new_service.chinese_service_name = request.POST.get('chinese_service_name')
            new_service.save()
            messages.success(request, 'New Service added successfully.')
            return redirect('extra_service')

    else:
        return render(request, 'administration/extra_service/add_extra_service.html')

def ferry_locations(request):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    ferry_locations = FerryLocation.objects.filter(host_name=request.user)
    context = {
        'ferry_locations': ferry_locations
    }
    return render(request, 'administration/ferry_location/ferry_location.html', context)

def add_ferry_location(request):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    if request.method == 'POST':
        if request.POST.get('location_name'):
            newlocation = FerryLocation()
            newlocation.location_name = request.POST.get('location_name')
            newlocation.host_name = request.user
            newlocation.save()
            messages.success(request, 'New Ferry Location added successfully.')
            return redirect('ferry_service')
        else:
            messages.error(request, 'Please complete all fields.')
            return redirect('ferry_service')
    else:
        return render(request, 'administration/ferry_location/add_ferry_location.html')

def role(request):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    role = Role.objects.order_by('id')
    context = {
        'role': role
    }
    return render(request, 'administration/role/role.html', context)

def add_role(request):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    if request.method == 'POST':

            new_role = Role()
            new_role.role_name = request.POST.get('role_name')
            new_role.active = request.POST.get('active')

            new_role.save()
            messages.success(request, 'New Role added successfully.')
            return redirect('role')

    else:
        return render(request, 'administration/role/add_role.html')

def driver(request):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    drivers = BusDriver.objects.filter(host=request.user)
    context = {
        'drivers': drivers
    }
    return render(request, 'administration/driver/driver.html', context)

def add_driver(request):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    if request.method == 'POST':
        if request.POST.get('name'):
            newdriver = BusDriver()
            newdriver.name = request.POST.get('name')
            newdriver.zawgyi_name = request.POST.get('zawgyi_name')
            newdriver.unicode_name = request.POST.get('unicode_name')
            newdriver.chinese_name = request.POST.get('chinese_name')
            newdriver.active = request.POST.get('active')
            newdriver.host = request.user
            newdriver.save()
            messages.success(request, 'New Driver Information added successfully.')
            return redirect('driver')
        else:
            messages.error(request, 'Please complete all fields.')
            return redirect('ferry_service')
    else:
        return render(request, 'administration/driver/add_driver.html')

def add_seats(request, id):
    if not request.user.is_authenticated:
        return redirect('login', permanent=True)

    bus = get_object_or_404(BusInfo, id=id)
    if not bus.host_name == request.user:
        return redirect('bus_list')
    if request.method == 'POST':
        new_seat = Seats()
        new_seat.seat_name = request.POST.get('seat_name')
        new_seat.seat_type = request.POST.get('seat_type')
        new_seat.bus = BusInfo.objects.get(id = id)
        new_seat.row_no = request.POST.get('row_no')
        new_seat.seat_no = request.POST.get('seat_no')
        new_seat.price_mmk = request.POST.get('price_mmk')
        new_seat.price_usd = request.POST.get('price_usd')

        new_seat.save()

        messages.success(request, 'New seat Information added successfully.')
        context = {
            'seats': Seats.objects.filter(bus=id).order_by('seat_name'),
            'id': id
        }

        return render(request, 'administration/bus/add_seat.html', context)

    else:

        context = {
            'seats': Seats.objects.filter(bus=id).order_by('seat_name')
        }

        return render(request, 'administration/bus/add_seat.html', context)

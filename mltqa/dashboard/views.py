import random
from django.shortcuts import render,redirect
from django.http import HttpRequest
from . import forms,models
from dotenv import dotenv_values
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from datetime import timedelta
from django.utils.timezone import now
from .firebase_config import bucket
from hijri_converter import convert
from django.utils import timezone
from django.utils.timezone import localtime
from urllib.parse import unquote, urlparse
from datetime import datetime

def dashboard_login_view(request:HttpRequest):

    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        email = request.POST['email']
        password = request.POST['password']

        if form.is_valid():
            try:
                admin = models.Admin.objects.get(email=email)
                if check_password(password, admin.password):
                    response = redirect("dashboard:dashboard_home_view")
                    response.set_cookie("admin", admin.id, max_age=60*60*24)

                    return response
                else:
                    form.add_error('password', 'كلمة المرور غير صحيحة ')
            except models.Admin.DoesNotExist:
                    form.add_error('email', 'البريد الالكتروني غير موجود ')

            else:
        
                form = forms.LoginForm() 

    else:
        form = forms.LoginForm()

    return render(request, 'dashboard/login.html', {
        "form": form,
    })


def dashboard_home_view(request:HttpRequest):
    if not 'admin' in request.COOKIES:
        return redirect('dashboard:dashboard_login_view')
    
    admin = models.Admin.objects.get(pk=request.COOKIES.get('admin'))
    number_of_new_requests = models.Request.objects.filter(created_at__gte=now() - timedelta(days=2)).count()
    total_events = models.Event.objects.count()
    total_active_events = models.Event.objects.filter(is_active=True).count()
    total_expired_events = models.Event.objects.filter(is_active=False).count()
    total_users= models.Request.objects.count()
    total_requests = models.Request.objects.count()
    total_admins= models.Request.objects.count()    



    if request.POST:
        pass

    return render(request, 'dashboard/panel/home.html', {
        "admin": admin,
        "number_of_new_requests": number_of_new_requests,
        "total_events": total_events,
        "total_active_events" :total_active_events,
        "total_expired_events":total_expired_events,
        "total_users":total_users,
        "total_requests":total_requests,
        "total_admins":total_admins,
    })

def format_arabic_hijri_with_time(dt):
    local_dt = timezone.localtime(dt)

    hijri = convert.Gregorian(
        local_dt.year,
        local_dt.month,
        local_dt.day
    ).to_hijri()

    hour = local_dt.hour
    minute = local_dt.minute
    period = "صباحاً" if hour < 12 else "مساءً"
    hour12 = hour if 1 <= hour <= 12 else abs(hour - 12) or 12

    time_str = f"{hour12}:{minute:02d} {period}"

    return f"{hijri.day} {hijri.month_name('ar')} {hijri.year} هـ - الساعة {time_str}"


def generateRandom(num: int):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    result = ''.join(random.choice(chars) for i in range(num))
    return result

def dashboard_events_view(request:HttpRequest):
    if not 'admin' in request.COOKIES:
        return redirect('dashboard:dashboard_login_view')
    
    success = False
    admin = models.Admin.objects.get(pk=request.COOKIES.get('admin'))

    if request.method == "POST":
        form = forms.EventForm(request.POST, request.FILES)

        if form.is_valid():
            image = request.FILES['image']
            random_name = generateRandom(10)
            filename = f"uploads/{random_name}.jpg" 

            image_url = upload_image(image, filename)

                
            new_event = models.Event(
                    title=request.POST['title'],
                    description=request.POST['description'],
                    location = request.POST['location'],
                    available_seats= request.POST['available_seats'],
                    start_datetime = datetime.strptime(request.POST['start_datetime'], '%Y-%m-%dT%H:%M'),
                    end_datetime = datetime.strptime(request.POST['end_datetime'], '%Y-%m-%dT%H:%M'),
                    created_by = admin,
                    is_active = True if request.POST.get('is_active') == 'on' else False,
                    image_url = image_url,
                    created_at = now()
                    
                )
            new_event.save()
            success = True
            form = forms.EventForm() 

    else:
        form = forms.EventForm()

    if "search" in request.GET:
        events = models.Event.objects.filter(title__contains=request.GET["search"])
    else:
        events = models.Event.objects.all()

    for event in events:
        for event in events:
            event.created_at_ar = format_arabic_hijri_with_time(event.created_at)
            event.startdate_ar = format_arabic_hijri_with_time(event.start_datetime)
            event.enddate_ar = format_arabic_hijri_with_time(event.end_datetime)

    number_of_new_requests = models.Request.objects.filter(created_at__gte=now() - timedelta(days=2)).count()
    return render(request, 'dashboard/panel/events.html',{
                "admin": admin,
                'events' : events,
                'form': form,
                'success': success,
                "number_of_new_requests": number_of_new_requests

    })


def dashboard_requests_view(request:HttpRequest):
    if request.POST:
        pass
    admin = models.Admin.objects.get(pk=request.COOKIES.get('admin'))
    number_of_new_requests = models.Request.objects.filter(created_at__gte=now() - timedelta(days=2)).count()
    return render(request, "dashboard/panel/requests.html",{
                "admin": admin,
                "number_of_new_requests": number_of_new_requests

    })

def dashboard_admins_view(request: HttpRequest):
    success = False
 
    if request.method == "POST":
        form = forms.AdminForm(request.POST)

        if form.is_valid():
            if request.POST['password'] != request.POST['confirm_password']:
                form.add_error('password', 'كلمات المرور غير متطابقة')
                form.add_error('confirm_password', 'كلمات المرور غير متطابقة')
                
            elif len(models.Admin.objects.filter(email=request.POST['email'])) > 0:
                form.add_error('email', 'البريد الالكتروني موجود مسبقا')


                
            else:
                new_admin = models.Admin(
                    full_name=request.POST['full_name'],
                    email=request.POST['email'],
                    password=make_password(request.POST['password'])
                )
                new_admin.save()
                success = True
                form = forms.AdminForm() 

    else:
        form = forms.AdminForm()

    if "search" in request.GET and len(request.GET["search"]) >= 3:
        admins = models.Admin.objects.filter(full_name__contains=request.GET["search"])
    else:
        admins = models.Admin.objects.all()

    admin = models.Admin.objects.get(pk=request.COOKIES.get('admin'))
    number_of_new_requests = models.Request.objects.filter(created_at__gte=now() - timedelta(days=2)).count()
    return render(request, "dashboard/panel/admins.html", {
        'admins' : admins,
        'form': form,
        'success': success,
        "admin": admin,
        "number_of_new_requests": number_of_new_requests

    })




def dashboard_event_delete_view(request:HttpRequest,id:int):
    event = models.Event.objects.get(pk=id)
    delete_image_from_firebase(event.image_url)

    if event:
        event.delete()
        return redirect('dashboard:dashboard_events_view')


def dashboard_event_edit_view(request:HttpRequest, id:int):
    try:
        event = models.Event.objects.get(pk=id)

        form = forms.EventForm()
        if event:
            admin = models.Admin.objects.get(pk=request.COOKIES.get('admin'))
            number_of_new_requests = models.Request.objects.filter(created_at__gte=now() - timedelta(days=2)).count()
            if request.method == "POST":
                    form = forms.EventForm(request.POST, request.FILES)
                    

                    if form.is_valid():
                        event.title = request.POST['title']
                        event.description = request.POST['description']
                        event.location = request.POST['location']
                        event.available_seats = request.POST['available_seats']
                        event.start_datetime = datetime.strptime(request.POST['start_datetime'], '%Y-%m-%dT%H:%M')
                        event.end_datetime = datetime.strptime(request.POST['end_datetime'], '%Y-%m-%dT%H:%M')
                        event.is_active = True if request.POST.get('is_active') == 'on' else False
                        if request.FILES and event.image_url:
                            delete_image_from_firebase(event.image_url)

                            image = request.FILES['image']
                            random_name = generateRandom(10)
                            filename = f"uploads/{random_name}.jpg" 

                            image_url = upload_image(image, filename)

                            event.image_url = image_url
                        event.save()
                        return redirect('dashboard:dashboard_events_view')
     
            data = {
        "id" : id,
        'title': event.title,
        'description': event.description,
        'image_url': event.image_url,
        'location': event.location,
        'available_seats': event.available_seats,
        'start_datetime': localtime(event.start_datetime).strftime('%Y-%m-%dT%H:%M'),
        'end_datetime': localtime(event.end_datetime).strftime('%Y-%m-%dT%H:%M'),
        'is_active': event.is_active,
            }
            return render(request, "dashboard/panel/edit_event.html", {
            'admin' : admin,
            "number_of_new_requests": number_of_new_requests,
            "data": data,
            "form": form,


                
            })
    except models.Event.DoesNotExist:
        return redirect('dashboard:dashboard_events_view')


def upload_image(uploadedFile, filename):

    blob = bucket.blob(filename) 

    blob.upload_from_string(uploadedFile.read(), content_type=uploadedFile.content_type)

    blob.make_public()

    return blob.public_url

def delete_image_from_firebase(image_url):
    try:
        path = urlparse(image_url).path
        encoded_path = path.split("/o/")[1].split("?")[0]
        file_path = unquote(encoded_path)  

        blob = bucket.blob(file_path)
        blob.delete()

    except Exception as e:
        print(" فشل حذف الصورة:", e)

def dashboard_admin_delete_view(request:HttpRequest,id:int):
    admin = models.Admin.objects.get(pk=id)
    if admin:
        admin.delete()
        return redirect('dashboard:dashboard_admins_view')



def dashboard_logout_view(request:HttpRequest):
    response = redirect("dashboard:dashboard_login_view")
    response.set_cookie("admin", 1, max_age=-3600)

    return response
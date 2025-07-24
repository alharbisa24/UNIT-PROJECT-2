from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from dashboard.models import *
from .models import *
from hijri_converter import convert
from django.utils import timezone
from . import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

def format_arabic_hijri_with_time(dt):
    local_dt = timezone.localtime(dt)

    hijri = convert.Gregorian(
        local_dt.year,
        local_dt.month,
        local_dt.day
    ).to_hijri()

    return f"{hijri.day} {hijri.month_name('ar')} {hijri.year}"

def home_view(request:HttpRequest):
    if 'user' in request.COOKIES:
        user = User.objects.get(pk=request.COOKIES.get('user'))
    else: 
         user = None
    events = Event.objects.all()[:3]
    
    for event in events:
        event.startdate_ar = format_arabic_hijri_with_time(event.start_datetime)
        event.enddate_ar = format_arabic_hijri_with_time(event.end_datetime)
        event.dateperiod = f"{event.startdate_ar} - {event.enddate_ar}"
        event.timeperiod = f"{event.start_datetime.strftime('%I:%M %p').replace('AM', 'صباحا').replace('PM', 'مساء')} - {event.end_datetime.strftime('%I:%M %p').replace('AM', 'صباحا').replace('PM', 'مساء')}"


    return render(request,"home/home.html", {
        "events": events,
        "user":user
    })


def events_view(request:HttpRequest):
    user = User.objects.get(pk=request.COOKIES.get('user'))
    return render(request,"home/allevents.html")

def event_details_view(request:HttpRequest, id:int):
    try: 
        event = Event.objects.get(pk=id)
        event.startdate_ar = format_arabic_hijri_with_time(event.start_datetime)
        event.enddate_ar = format_arabic_hijri_with_time(event.end_datetime)
        event.dateperiod = f"{event.startdate_ar} - {event.enddate_ar}"
        event.timeperiod = f"{event.start_datetime.strftime('%I:%M %p').replace('AM', 'صباحا').replace('PM', 'مساء')} - {event.end_datetime.strftime('%I:%M %p').replace('AM', 'صباحا').replace('PM', 'مساء')}"
    except Event.DoesNotExist:
         return redirect('home:home_view')
    
    success = request.GET.get('success', "false")
    error = request.GET.get('error', "error")
         

    return render(request,"home/event_details.html",{
        "event":event,
        "success": success,
        "error":error

    })


def login_view(request:HttpRequest):
    if request.method == "POST":
            form = forms.LoginForm(request.POST)
            email = request.POST['email']
            password = request.POST['password']

            if form.is_valid():
                try:
                    user = User.objects.get(email=email)
                    if check_password(password, user.password):
                        response = redirect("home:home_view")
                        response.set_cookie("user", user.id, max_age=60*60*24)

                        return response
                    else:
                        form.add_error('password', 'كلمة المرور غير صحيحة ')
                except User.DoesNotExist:
                        form.add_error('email', 'البريد الالكتروني غير موجود ')

                else:
            
                    form = forms.LoginForm() 

    else:
            form = forms.LoginForm()
            
    return render(request,"home/login.html")

def register_view(request:HttpRequest):
    if request.method == "POST":
        form = forms.RegisterForm(request.POST)

        if form.is_valid():
            if request.POST['password'] != request.POST['confirm_password']:
                form.add_error('password', 'كلمات المرور غير متطابقة')
                form.add_error('confirm_password', 'كلمات المرور غير متطابقة')
                
            elif len(User.objects.filter(email=request.POST['email'])) > 0:
                form.add_error('email', 'البريد الالكتروني موجود مسبقا')


                
            else:
                new_user = User(
                    full_name=request.POST['full_name'],
                    email=request.POST['email'],
                    phone=request.POST['phone'],
                    password=make_password(request.POST['password'])
                )
                new_user.save()
                form = forms.RegisterForm() 
                return redirect('home:login_view', {
                    "success":True
                })

    else:
        form = forms.RegisterForm()

    return render(request,"home/register.html",{
        "form":form
    })


def home_logout_view(request:HttpRequest):
    response = redirect("home:login_view")
    response.set_cookie("user", 1, max_age=-3600)

    return response


def book_event_request(request:HttpRequest,id:int):
     try:
          event = Event.objects.get(pk=id)
          user = User.objects.get(pk=request.COOKIES.get('user'))
          existing_request = Request.objects.filter(event=event, user=user).exists()
          if existing_request:
            return redirect(f'/event/{id}?error=exists')
          
          new_request = Request(event=event, user=user,accept_status=False)
          new_request.save()
          return redirect(f'/event/{id}?success=true')
          


     except Event.DoesNotExist:
            return redirect('home:home_view')


def requests_view(request:HttpRequest):
    user = User.objects.get(pk=request.COOKIES.get('user'))
    requests = user.user_requests.all()
    for req in requests:
        req.event.startdate_ar = format_arabic_hijri_with_time(req.event.start_datetime)
        req.event.enddate_ar = format_arabic_hijri_with_time(req.event.end_datetime)
        req.event.dateperiod = f"{req.event.startdate_ar} - {req.event.enddate_ar}"
        req.event.timeperiod = f"{req.event.start_datetime.strftime('%I:%M %p').replace('AM', 'صباحا').replace('PM', 'مساء')} - {req.event.end_datetime.strftime('%I:%M %p').replace('AM', 'صباحا').replace('PM', 'مساء')}"
   

    print(requests)
    return render(request, "home/requests.html", {
         "user":user,
         "requests":requests
     })
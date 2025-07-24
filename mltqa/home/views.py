from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from dashboard.models import *
from hijri_converter import convert
from django.utils import timezone


def format_arabic_hijri_with_time(dt):
    local_dt = timezone.localtime(dt)

    hijri = convert.Gregorian(
        local_dt.year,
        local_dt.month,
        local_dt.day
    ).to_hijri()

    return f"{hijri.day} {hijri.month_name('ar')} {hijri.year}"

def home_view(request:HttpRequest):
    events = Event.objects.all()[:3]
    
    for event in events:
        event.startdate_ar = format_arabic_hijri_with_time(event.start_datetime)
        event.enddate_ar = format_arabic_hijri_with_time(event.end_datetime)
        event.dateperiod = f"{event.startdate_ar} - {event.enddate_ar}"
        event.timeperiod = f"{event.start_datetime.strftime('%I:%M %p').replace('AM', 'صباحا').replace('PM', 'مساء')} - {event.end_datetime.strftime('%I:%M %p').replace('AM', 'صباحا').replace('PM', 'مساء')}"


    return render(request,"home/home.html", {
        "events": events
    })


def events_view(request:HttpRequest):
    return render(request,"home/allevents.html")

def event_details_view(request:HttpRequest, id:int):
    event = Event.objects.get(pk=id)
    event.startdate_ar = format_arabic_hijri_with_time(event.start_datetime)
    event.enddate_ar = format_arabic_hijri_with_time(event.end_datetime)
    event.dateperiod = f"{event.startdate_ar} - {event.enddate_ar}"
    event.timeperiod = f"{event.start_datetime.strftime('%I:%M %p').replace('AM', 'صباحا').replace('PM', 'مساء')} - {event.end_datetime.strftime('%I:%M %p').replace('AM', 'صباحا').replace('PM', 'مساء')}"


    return render(request,"home/event_details.html",{
        "event":event
    })


def login_view(request:HttpRequest):
    return render(request,"home/login.html")

def register_view(request:HttpRequest):
    return render(request,"home/register.html")
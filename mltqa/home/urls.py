from django.urls import path
from . import views

app_name= 'home'

urlpatterns = [
    path('', views.home_view, name="home_view"),
    path('login/', views.login_view, name="login_view"),
    path('register/', views.register_view, name="register_view"),
    path('events/', views.events_view, name="events_view"),
    path('event/<id>', views.event_details_view, name="event_details_view")
]
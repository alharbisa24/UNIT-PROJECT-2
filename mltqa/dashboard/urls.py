from django.urls import path
from . import views

app_name= "dashboard"

urlpatterns = [

    path('', views.dashboard_home_view, name="dashboard_home_view"),
    path('login/', views.dashboard_login_view, name="dashboard_login_view"),
    path('events/', views.dashboard_events_view, name="dashboard_events_view"),
    path('requests/', views.dashboard_requests_view, name="dashboard_requests_view"),
    path('admins/', views.dashboard_admins_view, name="dashboard_admins_view"),
    path('admins/<id>/delete/', views.dashboard_admin_delete_view, name="dashboard_admin_delete_view"),
    path('events/<id>/delete/', views.dashboard_event_delete_view, name="dashboard_event_delete_view"),
    path('logout/',views.dashboard_logout_view, name="dashboard_logout_view"),
    path('events/<id>/edit/', views.dashboard_event_edit_view, name="dashboard_event_edit_view")


]
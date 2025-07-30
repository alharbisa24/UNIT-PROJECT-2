from django.contrib import admin
from . import models as DashboardModels
# Register your models here.
admin.site.register(DashboardModels.Admin)
admin.site.register(DashboardModels.Event)
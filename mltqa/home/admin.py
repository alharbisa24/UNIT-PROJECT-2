from django.contrib import admin
from dashboard import models as DashboardModels
from home import models as HomeModels



# Register your models here.
admin.site.register(DashboardModels.Admin)
admin.site.register(DashboardModels.Event)
admin.site.register(HomeModels.Rating)
admin.site.register(HomeModels.User)
admin.site.register(HomeModels.Request)
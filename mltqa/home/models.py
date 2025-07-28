from django.db import models
from dashboard.models import * 
class User(models.Model):
    full_name=models.CharField(max_length=50)
    email=models.CharField(max_length=50,unique=True)
    phone=models.CharField(max_length=50,unique=True)
    password = models.TextField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)   

    def __str__(self):
        return self.full_name

class Request(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_requests')
    status = models.CharField(max_length=20,default="waiting")
    created_at = models.DateTimeField(auto_now_add=True)


 
    def __str__(self):
        return f"{self.user.full_name} - {self.event.title}"   

class Rating(models.Model):
    request = models.OneToOneField(Request,on_delete=models.CASCADE,related_name="request_rating")
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name="event_ratings")
    stars = models.IntegerField()
    comment = models.TextField(max_length=150)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.request.user.full_name} - {self.request.event.title} Rating"   
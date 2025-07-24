from django.db import models

class Admin(models.Model):
   full_name= models.CharField(max_length=50)
   email = models.TextField(max_length=50)
   password = models.TextField(max_length=50)
   created_at = models.DateTimeField(auto_now_add=True)
   def __str__(self):
        return self.full_name
    


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    image_url = models.URLField(null=True)
    location = models.CharField(max_length=255)
    available_seats = models.IntegerField(default=50)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    created_by = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='events')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



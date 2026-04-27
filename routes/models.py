from django.db import models
from django.contrib.auth.models import User

class Station(models.Model):
    name = models.CharField(max_length=64) 
    city = models.CharField(max_length=64) 

    def __str__(self):
        return f"{self.name} ({self.city})"

class Route(models.Model):
    origin = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="departures")
    
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="arrivals")
    
    duration = models.IntegerField()
    
    passengers = models.ManyToManyField(User, blank=True, related_name="booked_routes")

    def __str__(self):
        return f"{self.origin.name} to {self.destination.name}"
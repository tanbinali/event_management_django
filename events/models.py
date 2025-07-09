from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    rsvps = models.ManyToManyField(User, blank=True, related_name='rsvped_events')
    image = models.ImageField(
        upload_to='event_images/',
        default='event_images/default.jpg',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

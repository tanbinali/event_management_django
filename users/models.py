from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = CloudinaryField(
    'image',
    folder='profile_images',
    default='default_pfp.jpg',
    blank=True
)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", default="profile.jpeg")
    bio = models.TextField(blank=True, null=True)
   
    def __str__(self):
        return f"{self.user.username}Profile"
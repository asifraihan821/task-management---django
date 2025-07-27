from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


"""
class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name='userprofile', on_delete=models.CASCADE, primary_key=True)
    profile_image = models.ImageField(upload_to='profile_images',blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} profile"
    
"""
        
class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images', blank=True, default='profile_images/default_profile.jpg')
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username
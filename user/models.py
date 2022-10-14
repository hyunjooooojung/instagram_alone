from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import RegexValidator

# Create your models here.
class UserModel(AbstractUser):
    
    class Meta:
        db_table = "user"
        
    bio = models.TextField(max_length=256, default='')
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followee')
    profile = models.ImageField(blank= True, upload_to = "profile/")

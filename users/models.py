from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='profile_pics', default='avatar.svg')
    full_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username


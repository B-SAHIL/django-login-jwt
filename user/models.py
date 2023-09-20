from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from datetime import timedelta, date


# Create your models here.


class User(AbstractUser):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    trial_ended = models.DateField(default=date.today() + timedelta(days=30))
    first_name = models.CharField(max_length=20,  null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    full_name = models .CharField(max_length=40, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, default='')
    username = models.CharField(
        max_length=191, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True, default="")
    password = models.CharField(('password'), max_length=128, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.email)
    
    def save(self, *args, **kwargs):
        # Ensure that the username is set to the same value as the email
        self.username = self.email
        super().save(*args, **kwargs)

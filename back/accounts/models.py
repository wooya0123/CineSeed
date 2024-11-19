from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        UNDEFINED = 'UN', 'Undefined'
        DIRECTOR = 'DI', 'Director'
        ACTOR = 'AC', 'Actor'
        STAFF = 'ST', 'Staff'

    nickname = models.CharField(max_length=100)
    role = models.CharField(
        max_length=2,
        choices=Role.choices,
        default=Role.UNDEFINED
    )
    preference = models.CharField(max_length=250, blank=True)
    introduction = models.TextField(blank=True)
    profile_image = models.ImageField(blank=True, upload_to='images/')
    instagram = models.URLField(blank=True)
    etc = models.CharField(max_length=250, blank=True)

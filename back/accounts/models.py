from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # username = models.CharField(max_length=100)
    # password = models.CharField(max_length=100)
    class Role(models.TextChoices):
        DIRECTOR = 'DI', 'Director'
        ACTOR = 'AC', 'Actor'
        STAFF = 'ST', 'Staff'
        UNDEFINED = 'UN', 'Undefined'

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
    email = models.EmailField(blank=True)
    etc = models.CharField(max_length=250, blank=True)


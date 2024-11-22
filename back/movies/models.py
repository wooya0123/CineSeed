from django.db import models
from django.conf import settings

class Genre(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.code


class Movie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=250)
    image = models.ImageField(blank=True, upload_to='movie_poster/', default='images/default/thumbnail.png')
    start_date = models.DateField()
    end_date = models.DateField()
    movie_introduction = models.TextField()
    team_introduction = models.TextField(blank=True)
    budget_plan = models.TextField(blank=True)
    is_appliable = models.BooleanField(default=False)
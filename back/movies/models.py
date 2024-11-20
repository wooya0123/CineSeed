from django.db import models
from django.conf import settings

class Genre(models.Model):
    code = models.CharField(max_length=100)
    text = models.CharField(max_length=100)

class Movie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    image = models.ImageField(blank=True, upload_to='images/')
    start_date = models.DateField()
    end_date = models.DateField()
    movie_introduction = models.TextField()
    team_introduction = models.TextField()
    budget_plan = models.TextField()
    is_appliable = models.BooleanField()

class GameMovie(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(blank=True, upload_to='images/')

class GameQuestion(models.Model):
    type = models.CharField(max_length=100)
    question1 = models.CharField(max_length=250)
    question2 = models.CharField(max_length=250)
    question3 = models.CharField(max_length=250)
    question4 = models.CharField(max_length=250)
    question5 = models.CharField(max_length=250)
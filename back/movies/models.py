from django.db import models
from django.conf import settings

class Genre(models.Model):
    code = models.CharField(max_length=100)
    text = models.CharField(max_length=100)

def get_default_genre():
    return Genre.objects.get_or_create(code="X", text='미정')[0].id

class Movie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, default=get_default_genre, on_delete=models.SET_DEFAULT)
    title = models.CharField(max_length=250)
    image = models.ImageField(blank=True, upload_to='images/')
    start_date = models.DateField()
    end_date = models.DateField()
    movie_introduction = models.TextField()
    team_introduction = models.TextField()
    budget_plan = models.TextField()
    is_appliable = models.BooleanField()

class GameMovie(models.Model):
    genre = models.ForeignKey(Genre, default=get_default_genre, on_delete=models.SET_DEFAULT)
    title = models.CharField(max_length=100)
    image = models.ImageField(blank=True, upload_to='images/')

class GameQuestion(models.Model):
    type = models.CharField(max_length=100)
    question1_text = models.CharField(max_length=250)
    question1_a = models.CharField(max_length=250)
    question1_b = models.CharField(max_length=250)
    question2_text = models.CharField(max_length=250)
    question2_a = models.CharField(max_length=250)
    question2_b = models.CharField(max_length=250)
    question3_text = models.CharField(max_length=250)
    question3_a = models.CharField(max_length=250)
    question3_b = models.CharField(max_length=250)
    question4_text = models.CharField(max_length=250)
    question4_a = models.CharField(max_length=250)
    question4_b = models.CharField(max_length=250)
    question5_text = models.CharField(max_length=250)
    question5_a = models.CharField(max_length=250)
    question5_b = models.CharField(max_length=250)
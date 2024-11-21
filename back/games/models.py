from django.db import models
from movies.models import Genre

# Create your models here.
class GameMovie(models.Model):
    genre = models.ForeignKey(Genre, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=250)

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
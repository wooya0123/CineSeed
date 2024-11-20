from django.db import models
from django.conf import settings

class Genre(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=100)

class Movie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    image = models.ImageField(blank=True, upload_to='images/')
    start_date = models.DateField()
    end_date = models.DateField()
    movie_introduction = models.TextField()
    team_introduction = models.TextField()
    budget_plan = models.TextField()
    genres = models.ManyToManyField(Genre, through='MovieAndGenre',related_name='movies')

class GameMovie(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(blank=True, upload_to='images/')
    genres = models.ManyToManyField(Genre, through='GameMovieAndGenre',related_name='game_movies')

# movie - genre 중개테이블
class MovieAndGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        db_table = 'movies_and_genres'

# gamemovie - genre 중개테이블
class GameMovieAndGenre(models.Model):
    game_movie = models.ForeignKey(GameMovie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        db_table = 'game_movies_and_genres'
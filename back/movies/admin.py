from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Movie)
admin.site.register(models.GameMovie)
admin.site.register(models.Genre)
admin.site.register(models.MovieAndGenre)
admin.site.register(models.GameMovieAndGenre)

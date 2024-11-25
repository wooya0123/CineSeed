from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Movie, Genre

class User(AbstractUser):
    class Role(models.TextChoices):
        UNDEFINED = '미정', '미정'
        DIRECTOR = '감독', '감독'
        ACTOR = '배우', '배우'
        STAFF = '스탭', '스탭'
    
    # 안 쓰는 필드의 값은 null로 통일
    first_name = None
    last_name = None

    # 장르 필드는 기본값을 null로 설정
    genre = models.ForeignKey(
        Genre,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
        )
    nickname = models.CharField(max_length=100)
    role = models.CharField(
        max_length=2,
        choices=Role.choices,
        default=Role.UNDEFINED
    )
    introduction = models.TextField(blank=True)
    profile_image = models.ImageField(blank=True, upload_to='profile_images/', default='default_profile.png')
    instagram = models.URLField(blank=True)
    etc = models.CharField(max_length=250, blank=True)
    cash = models.IntegerField(default=1000000)
    title = models.CharField(max_length=100, blank=True)
    like_movies = models.ManyToManyField(Movie, through='LikeMovie', related_name='like_users')
    fund_movies = models.ManyToManyField(Movie, through='FundMovie', related_name='fund_users')
    apply_movies = models.ManyToManyField(Movie, through='ApplyMovie', related_name='apply_users')

class LikeMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    class Meta:
        db_table = 'like_movies'

class FundMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    amount = models.IntegerField()

    class Meta:
        db_table = 'fund_movies'

class ApplyMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        db_table = 'apply_movies'
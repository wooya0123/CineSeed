from rest_framework import serializers
from .models import Movie, Genre

class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude = ('movie_introduction', 'team_introduction', 'budget_plan',)
        read_only_fields = ('user', 'genre',)

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ('user', 'genre',)

class MovieCreateSerializer(serializers.ModelSerializer):
    # 외래키인 genre를 사용자가 입력할 수 있도록
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all())

    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ('user',)

class MovieUpdateSerializer(serializers.ModelSerializer):
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all())

    class Meta:
        model = Movie
        exclude = ('start_date', 'end_date',)
        read_only_fields = ('user',)
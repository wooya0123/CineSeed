from rest_framework import serializers
from .models import GameQuestion, GameMovie

class GameQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameQuestion
        fields = '__all__'

class GameMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameMovie
        fields = '__all__'
from rest_framework import serializers
from .models import GameQuestion

class GameQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameQuestion
        fields = '__all__'
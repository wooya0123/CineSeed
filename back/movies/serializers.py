from rest_framework import serializers
from .models import Movie, Genre
from accounts.models import FundMovie
from django.db.models import Sum

class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude = ('movie_introduction', 'team_introduction', 'budget_plan',)
        read_only_fields = ('user', 'genre',)

class MovieSerializer(serializers.ModelSerializer):
    # class FundMovieSerializer(serializers.ModelSerializer):
    #     class Meta:
    #         model = FundMovie
    #         fields = ['user_id', 'amount']

    # fund_users = FundMovieSerializer(source='fundmovie_set', many=True, read_only=True)

    fund_users = serializers.IntegerField(source='fundmovie_set.count', read_only=True)
    fund_amounts = serializers.SerializerMethodField('get_fund_amounts')
    
    # obj는 현재 serializer인 Movie 인스턴스
    def get_fund_amounts(self, obj):
        return obj.fundmovie_set.aggregate(Sum('amount'))['amount__sum']


    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ['user', 'genre', 'fund_amounts']

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


class MoviePopularSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)   # annotate로 추가된 필드

    class Meta:
        model = Movie
        fields = ('id', 'title', 'image', 'like_count')
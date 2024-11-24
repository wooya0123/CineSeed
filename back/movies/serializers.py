from rest_framework import serializers
from .models import Movie, Genre
from accounts.models import FundMovie
from django.db.models import Sum

class MovieListSerializer(serializers.ModelSerializer):
    genre = serializers.CharField(source='genre.name', read_only=True)
    user_nickname = serializers.CharField(source='user.nickname')
    profile_image = serializers.ImageField(source='user.profile_image')

    class Meta:
        model = Movie
        fields = ('id', 'user_nickname', 'profile_image', 'title', 'image', 'genre',)
        read_only_fields = ('user', 'genre',)

class MovieDetailSerializer(serializers.ModelSerializer):
    genre = serializers.CharField(source='genre.name', read_only=True)
    user_nickname = serializers.CharField(source='user.nickname')
    profile_image = serializers.ImageField(source='user.profile_image')

    fund_users = serializers.IntegerField(source='fundmovie_set.count', read_only=True)
    fund_amounts = serializers.SerializerMethodField('get_fund_amounts')

    # obj는 현재 serializer인 Movie 인스턴스
    def get_fund_amounts(self, obj):
        fund_amounts = obj.fundmovie_set.aggregate(Sum('amount'))['amount__sum']
        return fund_amounts if fund_amounts else 0

    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ['user', 'fund_amounts']

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


class MovieRecommendationSerializer(serializers.ModelSerializer):

    like_count = serializers.IntegerField(read_only=True)   # annotate로 추가된 필드
    genre = serializers.CharField(source='genre.name', read_only=True)
    user_nickname = serializers.CharField(source='user.nickname')
    profile_image = serializers.ImageField(source='user.profile_image')

    class Meta:
        model = Movie
        fields = ('id', 'user_nickname', 'profile_image', 'title', 'image', 'genre', 'like_count')
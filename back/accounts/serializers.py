from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from .models import User, Movie
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError

UserModel = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    genre = serializers.PrimaryKeyRelatedField(read_only=True, default=None)
    nickname = serializers.CharField(max_length=100, required=True)
    role = serializers.ChoiceField(choices=User.Role.choices, required=True)
    introduction = serializers.CharField(required=False, allow_blank=True)
    profile_image = serializers.ImageField(required=False)       # allow_blank 제거
    instagram = serializers.URLField(required=False, allow_blank=True)
    etc = serializers.CharField(max_length=250, required=False, allow_blank=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()   # 기본 username, password, email 불러오기
        data.update({
            'nickname': self.validated_data.get('nickname', ''),
            'role': self.validated_data.get('role', UserModel.Role.UNDEFINED),
            'introduction': self.validated_data.get('introduction', ''),
            'profile_image': self.validated_data.get('profile_image', None),
            'instagram': self.validated_data.get('instagram', ''),
            'etc': self.validated_data.get('etc', '')
        })
        return data

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()     # 커스텀한 필드들이 포함된 객체

        # user 객체에 기본 필드 설정
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.set_password(self.cleaned_data.get('password1'))

        # 커스텀한 필드를 user 객체에 넣기
        for key, value in self.cleaned_data.items():
            setattr(user, key, value)
        
        user.save()                             # 유저 객체를 db에 저장
        setup_user_email(request, user, [])     # 사용자 이메일 설정(이메일 확인)
        return user
    
    def validate(self, data):
        # 비밀번호 확인
        if data['password1'] != data['password2']:
            raise ValidationError({"password2": "passwords does not match"})
        return data
    
    
class CustomUserDetailsSerializer(UserDetailsSerializer):
    # 커스텀 필드 명시적 선언
    genre = serializers.PrimaryKeyRelatedField(read_only=True)
    nickname = serializers.CharField(max_length=100)
    role = serializers.ChoiceField(choices=User.Role.choices)
    introduction = serializers.CharField(allow_blank=True)
    profile_image = serializers.ImageField(required=False, allow_null=True)
    instagram = serializers.URLField(allow_blank=True)
    etc = serializers.CharField(max_length=250, allow_blank=True)

    class Meta:
        model = UserModel
        fields = (
            'pk',
            'username',
            'email',
            'first_name',
            'last_name',
            'genre',
            'nickname',
            'role',
            'introduction',
            'profile_image',
            'instagram',
            'etc'
        )
        read_only_fields = ('email',)

    def update(self, instance, validated_data):
        # 프로필 이미지 처리
        profile_image = validated_data.pop('profile_image', None)
        if profile_image:
            instance.profile_image = profile_image
        
        # 나머지 필드 업데이트
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    



class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title']  # 필요한 필드만 선택

class ApplyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname', 'role', 'introduction', 'profile_image', 'instagram', 'etc']

class MovieWithApplicantsSerializer(serializers.ModelSerializer):
    apply_users = ApplyUserSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'apply_users']


class DirectorProfileSerializer(serializers.ModelSerializer):
    like_movies = MovieSerializer(many=True, read_only=True)
    fund_movies = MovieSerializer(many=True, read_only=True)
    my_movie = MovieWithApplicantsSerializer(source='movie_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'nickname', 'role', 'introduction', 'profile_image', 'instagram', 'etc',
                  'title', 'like_movies', 'fund_movies', 'my_movie']



class ProfileSerializer(serializers.ModelSerializer):
    like_movies = MovieSerializer(many=True, read_only=True)
    fund_movies = MovieSerializer(many=True, read_only=True)
    apply_movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'nickname', 'role', 'introduction', 'profile_image', 'instagram', 'etc',
                  'cash', 'title', 'like_movies', 'fund_movies', 'apply_movies']
        

# class DirectorProfileSerializer(serializers.ModelSerializer):
#     class MovieIdSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = Movie
#             fields = ['id']


#     like_movies = MovieSerializer(many=True, read_only=True)
#     fund_movies = MovieSerializer(many=True, read_only=True)
#     my_movie = MovieSerializer(many=True, ) 


#     class Meta:
#         model = User
#         fields = ['id', 'nickname', 'role', 'introduction', 'profile_image', 'instagram', 'etc',
#                   'title', 'like_movies', 'fund_movies', ]
    
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(max_length=100, required=True)
    role = serializers.ChoiceField(choices=User.Role.choices, required=True)
    introduction = serializers.CharField(required=False, allow_blank=True)
    profile_image = serializers.ImageField(required=False)       # allow_blank 제거
    instagram = serializers.URLField(required=False, allow_blank=True)
    etc = serializers.CharField(max_length=250, required=False, allow_blank=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname', '')
        data['role'] = self.validated_data.get('role', User.Role.UNDEFINED)
        data['introduction'] = self.validated_data.get('introduction', '')
        data['profile_image'] = self.validated_data.get('profile_image', None)
        data['instagram'] = self.validated_data.get('instagram', '')
        data['etc'] = self.validated_data.get('etc', '')
        return data

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()

        # 기본 필드 설정
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.set_password(self.cleaned_data.get('password1'))

        # 커스텀 필드 설정
        user.nickname = self.cleaned_data.get('nickname')
        user.role = self.cleaned_data.get('role')
        user.introduction = self.cleaned_data.get('introduction')
        user.profile_image = self.cleaned_data.get('profile_image')
        user.instagram = self.cleaned_data.get('instagram')
        user.etc = self.cleaned_data.get('etc')
        user.save()
        setup_user_email(request, user, [])
        return user
    
class CustomUserDetailsSerializer(UserDetailsSerializer):
    # 커스텀 필드 명시적 선언
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
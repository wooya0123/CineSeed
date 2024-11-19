from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import User

class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(max_length=100, required=True)
    role = serializers.ChoiceField(choices=User.Role.choices, required=True)
    preference = serializers.CharField(max_length=250, required=False, allow_blank=True)
    introduction = serializers.CharField(required=False, allow_blank=True)
    profile_image = serializers.ImageField(required=False)  # allow_blank 제거
    instagram = serializers.URLField(required=False, allow_blank=True)  # allow_blank 추가
    etc = serializers.CharField(max_length=250, required=False, allow_blank=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname', '')
        data['role'] = self.validated_data.get('role', User.Role.UNDEFINED)
        data['preference'] = self.validated_data.get('preference', '')
        data['introduction'] = self.validated_data.get('introduction', '')
        data['profile_image'] = self.validated_data.get('profile_image', None)
        data['instagram'] = self.validated_data.get('instagram', '')
        data['etc'] = self.validated_data.get('etc', '')
        return data

    # def save(self, request):
    #     adapter = get_adapter()
    #     user = adapter.new_user(request)
    #     self.cleaned_data = self.get_cleaned_data()
    #     adapter.save_user(request, user, self)
    #     setup_user_email(request, user, [])
    #     user.nickname = self.cleaned_data.get('nickname')
    #     user.role = self.cleaned_data.get('role')
    #     user.preference = self.cleaned_data.get('preference')
    #     user.introduction = self.cleaned_data.get('introduction')
    #     user.profile_image = self.cleaned_data.get('profile_image')
    #     user.instagram = self.cleaned_data.get('instagram')
    #     user.etc = self.cleaned_data.get('etc')
    #     user.save()
    #     return user
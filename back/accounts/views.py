from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.contrib.auth import get_user_model
from .serializers import ProfileSerializer

@api_view(['GET', 'POST'])
def profile(request, user_id):
    User = get_user_model()
    user = User.objects.get(pk=user_id)      # 보고 있는 프로필의 유저

    if request.method == 'GET':
        serializer = ProfileSerializer(instance=user)
        print(serializer.data)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        pass


    


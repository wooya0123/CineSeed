from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.contrib.auth import get_user_model
from .serializers import ProfileSerializer

@api_view(['GET', 'PUT'])
def profile(request, user_id):
    User = get_user_model()
    user = User.objects.get(pk=user_id)      # 보고 있는 프로필의 유저

    # 프로필 페이지 조회
    if request.method == 'GET':
        serializer = ProfileSerializer(user)
        return Response(serializer.data)
    
    # 프로필 페이지 수정
    elif request.method == 'PUT':
        serializer = ProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()               # PUT에서는 read_only는 따로 저장 안해줘도 됨
        return Response(serializer.data)


    


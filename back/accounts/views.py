from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.contrib.auth import get_user_model
from .serializers import ProfileSerializer, DirectorProfileSerializer

# Permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request, user_id):
    User = get_user_model()
    user = User.objects.get(pk=user_id)     # 프로필의 유저
    request_user = User.objects.get(username=request.user)      # 수정하려는 유저
    request_user_id = request_user.id

    # 프로필 페이지 조회
    if request.method == 'GET':
        # 감독일 경우 지원한 영화 대신 지원자 정보를 보내줌
        if user.role == 'DI':
            serializer = DirectorProfileSerializer(user)
            return Response(serializer.data)
        
        # 그 외일 경우 지원한 영화 정보를 보내줌
        else:
            serializer = ProfileSerializer(user)
            return Response(serializer.data)
    
    # 프로필 페이지 수정
    elif request.method == 'PUT':
        serializer = ProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            if user.id == request_user_id:
                serializer.save()               # PUT에서는 read_only는 따로 저장 안해줘도 됨
                return Response(serializer.data)
            else:
                return Response({'message': '본인만 수정할 수 있습니다'}, status=status.HTTP_400_BAD_REQUEST)


    


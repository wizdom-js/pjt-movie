import re
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, FollowSerializer, ProfileSerializer, FollowerSerializer, ProfileChangeSerializer, PasswordChangeSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token
from .models import Feedback


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
	# 1-1. Client에서 온 데이터를 받아서
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')
		
	# 1-2. 패스워드 일치 여부 체크
    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
		
	# 2. UserSerializer를 통해 데이터 직렬화
    serializer = UserSerializer(data=request.data)
    
	# 3. validation 작업 진행 -> password도 같이 직렬화 진행
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        #4. 비밀번호 해싱 후 
        user.set_password(request.data.get('password'))
        user.save()
        # password는 직렬화 과정에는 포함 되지만 → 표현(response)할 때는 나타나지 않는다. (write_only)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def change_profile(request):
    user = request.user

    serializer = ProfileChangeSerializer(user, data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(profile_image=request.FILES['files'])
        return Response(serializer.data)


@api_view(['PUT'])
def change_password(request):
	# 1-1. Client에서 온 데이터를 받아서
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')
		
	# 1-2. 패스워드 일치 여부 체크
    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

	# 2. UserSerializer를 통해 데이터 직렬화
    user = request.user
    serializer = PasswordChangeSerializer(user, data=request.data)
    
	# 3. validation 작업 진행 -> password도 같이 직렬화 진행
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        # #4. 비밀번호 해싱 후 
        user.set_password(request.data.get('password'))
        user.save()
        # password는 직렬화 과정에는 포함 되지만 → 표현(response)할 때는 나타나지 않는다. (write_only)
        return Response(serializer.data)
    return Response({ 'detail': '잘못된 요청입니다.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    serializer = ProfileSerializer(person)

    return Response(serializer.data)
    

@api_view(['POST'])
def follow(request, username):
    # POST 요청일 경우는 바뀐 팔로우 정보만 넘겨받으면 된다.
    if request.user.is_authenticated:
        me = request.user
        you = get_object_or_404(get_user_model(), username=username)
        # 너와 내가 다른 사람이여야 팔로우를 진행할 수 있음
        # 나 자신은 팔로우해서는 안됨
        if me != you:
            # 내가 상대방(person)의 팔로워 목록에 있다면
            if you.followers.filter(pk=me.pk).exists():
            # 언팔로우
                you.followers.remove(me)
                followed = False
            else:
            # 팔로우
                you.followers.add(me)
                followed = True

        temp = {
            'followed': followed,
            # 프론트에서 필요없다고 판단 (새로고침 하기 전에는 일부러 바뀌지 않게 의도)
            # 'followers_count': you.followers.count(),
            # 'followings_count': you.followings.count()
        }

        return JsonResponse(temp)
    return Response({ 'detail': '인증되지 않은 사용자 입니다.'}, status=status.HTTP_401_UNAUTHORIZED)
    


@api_view(['POST'])
def delete_follower(request, me_username, you_username):
    # if request.method == 'POST':
    if request.user.is_authenticated:
        me = request.user
        you = get_object_or_404(get_user_model(), username=me_username)
        target = get_object_or_404(get_user_model(), username=you_username)
        # 로그인한 사용자 == 지금 보고있는 프로필 이라면 권한이 생긴다
        if me == you:
            # 내 팔로워 목록중에 타겟이 있다면
            if you.followers.filter(pk=target.pk).exists():
            # 죽여
                you.followers.remove(target)

            serializer = FollowerSerializer(you)

            return JsonResponse(serializer.data)
        return Response({ 'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({ 'detail': '인증되지 않은 사용자 입니다.' }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['DELETE'])
def withdrawal(request):
    Feedback.objects.create(user=request.user.username, feedback=request.data['detailReason'], reason=request.data['reason'])
    request.user.delete()

    return Response({ 'detail': '회원탈퇴가 완료되었습니다.'}, status=status.HTTP_200_OK)


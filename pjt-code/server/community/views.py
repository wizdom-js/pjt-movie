from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, PostListSerializer, PostDetailSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.core.paginator import Paginator


# Create your views here.
# GET일때 게시글 받아오기, POST 일때 게시글 생성
@api_view(['GET'])
@permission_classes([AllowAny])
def post_list(request):
    # 모델 db에서 다 가져와서 JSON으로 넘겨
    # posts = get_list_or_404(Post)
    posts = Post.objects.order_by('-pk')
    paginator = Paginator(posts, 10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    serializer = PostListSerializer(page_obj, many=True)
    data = serializer.data
    data.append({'possible_page': paginator.num_pages})
    return Response(data)

@api_view(['POST'])
def post_create(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):

        serializer.save(user=request.user) # 어떤유저가 썼는지도 같이보내
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def post_get_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    # 현재 좋아요를 요청하는 회원(request.user)이
    # 해당 게시글의 좋아요를 누른 회원 목록에 이미 있다면,
    if post.like_users.filter(pk=request.user.pk).exists():
        is_liked = True
    else:
        is_liked = False

    serializer = PostDetailSerializer(post)
    data = serializer.data
    data.update({'is_liked': is_liked})
 
    return Response(data)

# PUT일때 게시글 수정, DELETE일때 게시글 삭제
@api_view(['PUT', 'DELETE'])
def post_update_delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if not request.user.post_set.filter(pk=post_pk).exists():
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDON)

    if request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        post.delete()
        return Response({ 'id': post_pk }, status=status.HTTP_204_NO_CONTENT)

# GET 요청일때 댓글 가져오기, POST요청일때 댓글 작성
@api_view(['GET'])
@permission_classes([AllowAny])
def comment_list(request, post_pk):
    # 모델 db에서 다 가져와서 JSON으로 넘겨
    comments = Comment.objects.filter(post_id=post_pk).order_by('-pk')
    
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def comment_create(request, post_pk):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):

        serializer.save(user=request.user, post_id=post_pk) # 어떤유저가 썼는지도 같이보내
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# PUT일때 댓글 수정, DELETE일때 댓글 삭제
@api_view(['PUT', 'DELETE'])
def comment_update_delete(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, post_id=post_pk, pk=comment_pk)

    if not request.user.comment_set.filter(pk=comment_pk).exists():
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDON)

    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        comment.delete()
        return Response({ 'post_id': post_pk, 'comment_id': comment_pk }, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def likes(request, post_pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_pk)
        # 현재 좋아요를 요청하는 회원(request.user)이
        # 해당 게시글의 좋아요를 누른 회원 목록에 이미 있다면,
        if post.like_users.filter(pk=request.user.pk).exists():
        # if request.user in article.like_users.all(): 
            # 좋아요 취소
            post.like_users.remove(request.user)
            post.is_liked = False
        else:
            # 좋아요 하기
            post.like_users.add(request.user)
            post.is_liked = True
        post.save()
        context = {
            'liked': post.is_liked,
            'count': post.like_users.count()
        }
        return Response(context)
    return Response({ 'detail': '인증되지 않은 사용자 입니다.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([AllowAny])
def search(request, word):
    posts = Post.objects.filter(title__icontains=word).order_by('-pk')
    serializer = PostListSerializer(posts, many=True)
    return Response(serializer.data)
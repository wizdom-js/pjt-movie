from django.urls import path
from . import views

urlpatterns = [
    path('',views.post_list),    # (GET) 게시글 전체 리스트 받아오기
    path('post/', views.post_create),   # (POST) 게시글 작성
    path('<int:post_pk>/',views.post_update_delete), # (PUT) 게시글 업데이트, (DELETE) 게시글 삭제
    path('<int:post_pk>/detail/',views.post_get_detail),     # (GET) 게시글 상세 조회
    path('<int:post_pk>/comment_list/', views.comment_list),  # (GET) 댓글 전체 리스트 받아오기
    path('<int:post_pk>/comment_create/', views.comment_create),  # (POST) 댓글 작성

    path('<int:post_pk>/likes/', views.likes),  # (POSt) 게시글 좋아요 or 좋아요 취소
    path('<int:post_pk>/comment/<int:comment_pk>/', views.comment_update_delete),   # (PUT) 댓글 업데이트, (DELETE) 댓글 삭제
    path('<word>/search/', views.search),   # (GET) 게시글 검색
]
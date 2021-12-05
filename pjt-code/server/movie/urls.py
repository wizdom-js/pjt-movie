from django.urls import path
from . import views

urlpatterns = [
    path('<movie_id>/detail/', views.detail),   # (GET) 영화 상세정보 받기, TMDB API
    path('<movie_id>/recommend/', views.recommend),   # (GET) 한 영화(movie_id)에 관련한 추천영화들 목록 제공 (20개 이하), TMDB API
    path('<movie_id>/similar/', views.similar),   # (GET) 한 영화(movie_id)와 비슷한 영화들(장르, 키워드기준) 목록 제공 (20개 이하), TMDB API
    path('popular/', views.popular),     # (GET) 인기있는 영화 받기 TOP20, TMDB API
    # path('latest/', views.latest)       # (GET) 최신 영화 받기(진짜 방금생긴 영화 딱 한개), TMDB API
    path('now_playing/', views.now_playing),     # (GET) 현재 상영중인 영화 받기 20개, TMDB API
    path('top_rated/', views.top_rated),    # (GET) 가장 평점 높은 영화 받기 TOP20, TMDB API
    path('upcoming/', views.upcoming),   # (GET) 개봉 예정인 영화 받기 20개, TMDB API
    path('<word>/search/', views.search), # (GET) word가 포함된영화 검색
    path('<movie_id>/like/', views.like),   # (POST)영화 좋아요

    path('<movie_id>/review_list/', views.review_list),  # (GET) 리뷰 전체 리스트 받아오기,
    path('<movie_id>/review_create/', views.review_create),  # (POST) 리뷰 작성
    path('<movie_id>/review/<int:review_pk>/', views.review_update_delete),   # (PUT) 리뷰 업데이트, (DELETE) 리뷰 삭제

    path('signup_like/', views.signup_like),    # (POST) 회원가입시 받은 관심장르별로 영화 5개씩 묶어서 주기   
    path('weather_recommend/', views.weather_recommend), # (POST) 날씨에 따른 영화 추천
    path('time_recommend/', views.time_recommend), # (GEt) 시간대에 따른 영화 추천
    path('YNs_recommend/', views.YNs_recommend), # (GET) 영남s 알고리즘에 의한 추천
]
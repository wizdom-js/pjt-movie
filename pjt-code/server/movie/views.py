from django.contrib.auth import get_user_model
from django.shortcuts import  get_object_or_404, get_list_or_404, render
import requests
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from .serializers import LikeSerializer, ReviewSerializer, CrawledMovieSerializer
from .models import Like, Review, CrawledMovie
from django.core.paginator import Paginator
import random
from datetime import datetime
from django.db.models import Q


def get_request_url(method='/movie/popular', **kwargs):
        api_key = '7682372ec7f0caa4ebe6d64b807d5293'
        """API 요청에 필요한 주소를 구성합니다.
        
        Args:
            method: API 서비스에서 제공하는 메서드로써 기본 경로 뒤에 추가됩니다.
            **kwargs: 쿼리 스트링 형태로 기본 요청 주소 뒤에 추가됩니다.

        Returns:
            base_url, 메서드, 쿼리 스트링으로 구성된 요청 주소를 반환합니다.
        """
        base_url = 'https://api.themoviedb.org/3'
        request_url = base_url + method
        request_url += f'?api_key={api_key}'

        for k, v in kwargs.items():
            request_url += f'&{k}={v}'

        return request_url


# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny])
def detail(request, movie_id):
    detail_url = get_request_url(f'/movie/{movie_id}', language='ko-KR')
    video_url = get_request_url(f'/movie/{movie_id}/videos', language='ko-KR')

    data = requests.get(detail_url).json()
    data2 = requests.get(video_url).json()
    results = data2['results']
    video = []
    for i in range(len(results)):
        video.append(
            {
                'name': results[i]['name'],
                'video_id': results[i]['key'],
                'type': results[i]['type']
            }
        )    


    if not Like.objects.filter(user_id=request.user.pk).exists():
            liked = False
    else:
        # 테이블에 내가 좋아요한 영화가 존재한다면
        mylikes = Like.objects.filter(user_id=request.user.pk)
        # 내가 좋아요한 영화중에 지금 좋아요 하려는 영화가 없다면?
        if not mylikes.filter(movie_id=movie_id).exists():
            liked = False
        else:
            # 내가 좋아요한 영화중에 내가 좋아요 하려는 영화가 있다면?
            liked = True

    if data['status'] == 'Rumored':
        movie_status = ''
    elif data['status'] == 'Planned':
        movie_status = '계획'
    elif data['status'] == 'In Production':
        movie_status = '제작 중'
    elif data['status'] == 'Post Production':
        movie_status = '제작 예정'
    elif data['status'] == 'Released':
        movie_status = '개봉'
    elif data['status'] == 'Canceled':
        movie_status = '개봉 취소'

    context = {
        'movie_id': data['id'],
        'title': data['title'],
        'tagline': data['tagline'],
        'genres': data['genres'],
        'overview': data['overview'],
        'poster_path': data['poster_path'],
        'adult': data['adult'],
        'vote_average': data['vote_average'],
        'vote_count': data['vote_count'],
        'release_date': data['release_date'],
        'status': movie_status,
        'runtime': data['runtime'],
        'video': video,
        'liked': liked,
        'like_count': Like.objects.filter(movie_id=movie_id).count()
    }

    return Response(context)

@api_view(['GET'])
@permission_classes([AllowAny])
def recommend(request, movie_id):
    recommend_url = get_request_url(f'/movie/{movie_id}/recommendations', language='ko-KR')

    data = requests.get(recommend_url).json()
    results = data['results']

    return Response(results)


@api_view(['GET'])
@permission_classes([AllowAny])
def similar(request, movie_id):
    similar_url = get_request_url(f'/movie/{movie_id}/similar', language='ko-KR')

    data = requests.get(similar_url).json()
    results = data['results']

    return Response(results)


@api_view(['GET'])
@permission_classes([AllowAny])
def popular(request):
    popular_url = get_request_url('/movie/popular', language='ko-KR', region='KR')
    data = requests.get(popular_url).json()
    results = data['results']

    return Response(results)

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def latest(request):
#     latest_url = get_request_url(f'/movie/latest', language='ko-KR')
#     data = requests.get(latest_url).json()
    
#     # print(results)
#     return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def now_playing(request):
    now_playing_url = get_request_url('/movie/now_playing', language='ko-KR', region='KR')
    data = requests.get(now_playing_url).json()
    results = data['results']

    return Response(results)


@api_view(['GET'])
@permission_classes([AllowAny])
def top_rated(request):
    top_rated_url = get_request_url('/movie/top_rated', language='ko-KR', region='KR')
    data = requests.get(top_rated_url).json()
    results = data['results']

    return Response(results)


@api_view(['GET'])
@permission_classes([AllowAny])
def upcoming(request):
    upcoming_url = get_request_url('/movie/upcoming',language='ko-KR', region='KR')
    data = requests.get(upcoming_url).json()
    results = data['results']

    return Response(results)

@api_view(['GET'])
@permission_classes([AllowAny])
def search(request, word):
    upcoming_url = get_request_url('/search/movie', query=f'{word}', language='ko-KR', region='KR')
    data = requests.get(upcoming_url).json()
    results = data['results']

    return Response(results)


@api_view(['POST'])
def like(request, movie_id):
    if request.user.is_authenticated:
        detail_url = get_request_url(f'/movie/{movie_id}', language='ko-KR')
        data = requests.get(detail_url).json()
        
        # 테이블에 내가 좋아요한 영화가 아무것도 없다면
        if not Like.objects.filter(user_id=request.user.pk).exists():
            Like.objects.create(user_id=request.user.pk, movie_id=movie_id, like_poster_path=data['poster_path'], like_movie_title=data['title'])
            liked = True
        else:
            # 테이블에 내가 좋아요한 영화가 존재한다면
            mylikes = Like.objects.filter(user_id=request.user.pk)
            # 내가 좋아요한 영화중에 지금 좋아요 하려는 영화가 없다면?
            if not mylikes.filter(movie_id=movie_id).exists():
                Like.objects.create(user_id=request.user.pk, movie_id=movie_id, like_poster_path=data['poster_path'], like_movie_title=data['title']) # 추가
                liked = True
            else:
                # 내가 좋아요한 영화중에 내가 좋아요 하려는 영화가 있다면?
                mylikes.filter(movie_id=movie_id).delete() # 사쿠죠
                liked = False
        context = {
            'liked': liked,
            'count': Like.objects.filter(movie_id=movie_id).count()
        }
        return Response(context)
    return Response({ 'detail': '인증되지 않은 사용자 입니다.' }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([AllowAny])
def review_list(request, movie_id):
    # 모델 db에서 다 가져와서 JSON으로 넘겨
    # reviews = get_list_or_404(Review.objects.order_by('-pk'), movie_id=movie_id)
    reviews = Review.objects.filter(movie_id=movie_id).order_by('-pk')
    serializer = ReviewSerializer(reviews, many=True)
    data = serializer.data
    return Response(data)

@api_view(['POST'])
def review_create(request, movie_id):
    detail_url = get_request_url(f'/movie/{movie_id}', language='ko-KR')
    data = requests.get(detail_url).json()
        
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):

        serializer.save(user=request.user, movie_id=movie_id, poster_path=data['poster_path'], movie_title=data['title']) # 어떤유저가 썼는지도 같이보내
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# PUT일때 리뷰 수정, DELETE일때 리뷰 삭제A
@api_view(['PUT', 'DELETE'])
def review_update_delete(request, movie_id, review_pk):
    review = get_object_or_404(Review, movie_id=movie_id, pk=review_pk)

    if not request.user.review_set.filter(pk=review_pk).exists():
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDON)

    if request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        review.delete()
        return Response({ 'movie_id': movie_id, 'review_id': review_pk }, status=status.HTTP_204_NO_CONTENT)


# Vue에서 실험 필요, POST맨에서 form-data로 배열을 못전하는거같애
@api_view(['POST'])
@permission_classes([AllowAny])
def signup_like(request):
    print(request.data)
    genres = request.data
    
    context = {}
    for genre in genres:
        detail_url = get_request_url(f'/discover/movie', language='ko-KR')
        detail_url += f'&with_genres={genre}'
        data = requests.get(detail_url).json()
        results = data['results'][:5]
        temp = []
        for result in results:
            temp.append(
                {
                'movie_id': result['id'],
                'title': result['title'],
                'poster_path': result['poster_path'],
                'genre_ids': result['genre_ids']
                }
            )
        context[genre] = temp
        print(context)

    return Response(context)


'''
SF878, TV 영화10770, 가족10751, 공포27, 다큐멘터리99, 드라마18, 
로맨스10749, 모험12, 미스터리9648, 범죄80, 서부37, 스릴러53, 
애니메이션16, 액션28, 역사36, 음악10402, 판타지14, 전쟁10752, 코미디35
'''
sentimental = ['18', '10402', '14', '10749']
gloomy = ['27', '80', '53', '10752', '9648']
fierce = ['878', '27', '80', '53', '10752']
scary = ['27', '80', '53']
innocent = ['10402', '35', '10752']
positive = ['878', '18', '10749', '28', '10402', '14', '10751', '35']

weather_code = {
    'Thunderstorm': fierce,
    'Drizzle': sentimental,
    'Rain': sentimental + scary,
    'Snow': sentimental + innocent,
    'Atmosphere': gloomy + fierce,
    'Clear': positive,
    'Clouds': gloomy
}


@api_view(['POST'])
@permission_classes([AllowAny])
def weather_recommend(request):
    # weather = request.data['weather']
    weather = request.data.get('weather')
    genre = random.sample(weather_code[weather], 3)
    genre = ','.join(genre)

    movie_url = get_request_url(f'/discover/movie', language='ko-KR')
    movie_url += f'&with_genres={genre}&watch_region=KR'
    data = requests.get(movie_url).json()

    results = [
        {
            'weather': weather
        }
    ]

    results.append(data['results'])

    return Response(results)

time = {
    'dawn': sentimental + innocent + scary + gloomy,
    'morning': positive + innocent,
    'afternoon': positive + fierce,
    'dinner': sentimental + innocent,
    'night': scary + gloomy + sentimental + innocent,
}

@api_view(['GET'])
@permission_classes([AllowAny])
def time_recommend(request):
    current_time = datetime.now().hour # 0~ 23
    if 1 <= current_time < 7:
        now = 'dawn'
    elif 7 <= current_time < 12:
        now = 'morning'
    elif 12 <= current_time < 18:
        now = 'afternoon'
    elif 18 <= current_time < 22:
        now = 'dinner'
    else:
        now = 'night'
    
    genre = random.sample(time[now], 3)
    genre = ','.join(genre)

    movie_url = get_request_url(f'/discover/movie', language='ko-KR')
    movie_url += f'&with_genres={genre}&watch_region=KR'
    data = requests.get(movie_url).json()

    results = [
        {
            'now': now,
            'current_time': current_time
        }
    ]

    results.append(data['results'])

    return Response(results)

# 내가 리뷰한 영화의 장르,국가, 내가 준 점수 기반 추천
@api_view(['GET'])
@permission_classes([AllowAny])
def YNs_recommend(request):
    #내가 리뷰남긴 영화 가져오기
    reviewmovies = Review.objects.filter(user=request.user)
    serializer = ReviewSerializer(reviewmovies, many=True)
    data = serializer.data
    if len(data) == 0:
        return Response({detail: '등록한 리뷰가 없습니다'})
    else:
        arr = []
        rank_arr = []
        for i in range(len(data)):
            # print(data[i]['movie_id']) # 된다!
            movie_id = data[i]['movie_id']
            rank_arr.append(data[i]['rank'])
            detail_url = get_request_url(f'/movie/{movie_id}', language='ko-KR')
            result = requests.get(detail_url).json()
            arr.append(result) # for문을 다 돌면 arr에 내가 좋아요한 영화들 json데이터들 쌓여있음

        v = [{} for i in range(100000)]
        # 각 노드마다 rating, rating_list가 있음
        rating = [3 for i in range(100000)] # 각 노드에서 rating_list의 평균
        rating_list = [[3] for i in range(100000)]  # 누가 어떤 영화에 점수를 매기면 위의 트리를 타고 내려오면서 rating_list에 추가

        # 장르레벨 세팅
        # genre_ids = ['878', '10770', '10751', '27', '99', '18', '10749', '12', '9648', '80', '37', '53', '16', '28', '36', '10402', '14', '10752', '35']
        genre_ids = ['SF', 'TV 영화', '가족', '공포', '다큐멘터리', '드라마', '로맨스', '모험', '미스터리', '범죄', '서부', '스릴러', '애니메이션', '액션', '역사', '음악', '판타지', '전쟁', '코미디']
        node = 1
        # 일단 장르레벨 노드들 고유한 번호를 하나하나 부여해
        # 루트에서부터 처음 장르로 타고 내려갈때 이름가지고 인덱스로 찾아갈수 있게  
        for i in genre_ids:
            v[0][i] = node
            node += 1

        # 국가레벨 세팅
        country = []
        for i in range(len(arr)):
            for j in arr[i]['production_countries']:
                country.append(j['name'])
        country = list(set(country))
        # print(country)

        # 그다음 레벨(국가)의 시작번호가 node_num
        node_num = node

        movie_list = [[] for i in range(100000)]

        # 지금 장르는 node개만큼 있으니까 for문 node번 돌면서 장르 밑에 국가 하나하나 다 달아
        for i in range(1, node):
            for j in country:
                v[i][j] = node_num
                node_num += 1
        # v[0][i[0]] : 장르 노드 번호
        # v[v[0][i[0]][i[1]] : 국가 노드 번호

        # cur = v[v[0][i[0]]][i[1]]   # 국가까지 내려왔어
        for i in range(len(arr)):
            for j in arr[i]['genres']: # arr의 i번째의 장르들 순회
                for k in arr[i]['production_countries']: # 장르타고 왔어 이제 국가들 순회
                    cur =v[v[0][str(j['name'])]][k['name']]
                    movie_list[cur].append([arr[i]['id'], arr[i]['popularity']]) # 내가 리뷰한 영화의 정보를 기저노드에 저장시켜.
                    # 기저노드에 [movie_id, 인기도(정렬목적)]
                    # print(cur, i['id'], i['popularity'], i[])


        def dfs(cur, depth, total):
            total += rating[cur]

            # 다 내려왔어?
            if depth == 2:
                for i in movie_list[cur]:
                    recom_list.append([total, -i[1], i[0], arr[:]]) # 감독까지 다 내려왔을때의 점수합과, 그 경로의 영화의 id
                
                return

            for i in v[cur]:
                arr.append(i)
                dfs(v[cur][i], depth + 1, total)
                arr.pop()

        #movie_info : ["장르", "국가", "감독", "평점", "영화 이름"]
        for i in range(len(arr)):
            for j in arr[i]['genres']: # arr의 i번째의 장르들 순회
                for k in arr[i]['production_countries']: # 장르타고 왔어 이제 국가들 순회
                    # 루트
                    cur = 0
                    # rating_list[cur].append(movie_info[3])
                    # rating[cur] = sum(rating_list[cur]) / len(rating_list[cur])

                    cur = v[cur][str(j['name'])] # 한단계 내려가
                    # 장르
                    rating_list[cur].append(rank_arr[i])
                    rating[cur] = sum(rating_list[cur]) / len(rating_list[cur])

                    cur = v[cur][k['name']]
                    # 국가
                    rating_list[cur].append(rank_arr[i])
                    rating[cur] = sum(rating_list[cur]) / len(rating_list[cur])


        # 다업데이트 했어
        recom_list = []
        arr = []
        dfs(0, 0, 0)
        recom_list.sort(reverse=True)
        # print(recom_list)
        # seen_id = recom_list[0][2]
        # best_genre = recom_list[0][3][0]
        # best_country = recom_list[0][3][1]
        # print(best)
        # best_url = get_request_url(f'/movie/{best_id}', language='ko-KR')
        # result = requests.get(best_url).json()
        # print(seen_id, best_genre, best_country)
        seen_arr = []
        genre_arr = []
        country_arr = []
        for i in range(len(recom_list)):
            temp = recom_list[i][3][0]
            if temp not in genre_arr:
                genre_arr.append(temp)
            temp = recom_list[i][3][1]
            if temp not in country_arr:
                country_arr.append(temp)
            temp = recom_list[i][2]
            if temp not in seen_arr:
                seen_arr.append(temp)
            if i == 4:
                break

        # recommend_movie = CrawledMovie.objects.filter((Q(genre_1__in=best_genre_arr)|Q(genre_2__in=best_genre_arr)|Q(genre_3__in=best_genre_arr)|Q(genre_4__in=best_genre_arr))&(Q(country_1__in=best_country_arr)|Q(country_2__in=best_country_arr)|Q(country_3__in=best_country_arr))).order_by('-popularity')[:20]

        # bestserializer = CrawledMovieSerializer(recommend_movie, many=True)

        # return Response({'아무거나': 1232})
        recommend_movie = CrawledMovie.objects.filter(backdrop_path__isnull=False).filter((Q(genre_1__in=genre_arr)|Q(genre_2__in=genre_arr)|Q(genre_3__in=genre_arr)|Q(genre_4__in=genre_arr))&(Q(country_1__in=country_arr)|Q(country_2__in=country_arr)|Q(country_3__in=country_arr))).exclude(movie_id__in=seen_arr).order_by('-popularity')[:20]

        bestserializer = CrawledMovieSerializer(recommend_movie, many=True)
        print(bestserializer)
        return Response(bestserializer.data)
    
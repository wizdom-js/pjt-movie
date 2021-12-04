<template>
  <v-container>
    <v-row>
      <div class="d-flex flex-column align-items-center justify-center my-3">
        <h1>{{ movieData.title }}</h1>
        <p>{{ movieData.tagline }}</p>
      </div>
      <v-col cols="4">
        <img :src="posterPath" :alt="`${movieData.title} 포스터`" width="100%">
        <!-- <img :src="require(`@/assets/ticket.png`)" alt="" width="100%"> -->
        <div class="d-flex justify-center align-items-center flex-column my-5">
          <!-- 좋아요 -->
          <div @click="changeLike" class="d-flex align-items-end jusitify-end my-3">
            <div v-if="likeState"><v-icon color="red" large>mdi-heart</v-icon>좋아요 취소</div>
            <div v-else><v-icon color="red">mdi-heart-outline</v-icon>좋아요</div>
            <div class="mx-3">{{ likeCount }}</div>
          </div>
          <v-divider></v-divider>
          <!-- 평점 -->
          <div class="d-flex align-items-end">
            <v-rating background-color="grey" color="warning"
              length="5" readonly half-increments
              large v-model="rating" 
            ></v-rating>
            <div class="px-3 text-h4">{{ rating }}</div>
            <div>{{ movieData.vote_count }}명</div>
          </div>
        </div>
      </v-col>
      <v-col cols="8">
        <v-expansion-panels focusable multiple v-model="panel">
          <!-- 영화정보 -->
          <v-expansion-panel>
            <v-expansion-panel-header>
              "{{ movieData.title }}" INFO
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <!-- 개요 -->
              <div class="d-flex align-items-end my-5">
                <div class="me-1">개요 |장르:</div>
                <div
                  v-for="genre in genres"
                  :key="genre"
                  class="mx-1"
                >{{ genre }}</div> |
                <div class="me-1">런타임: {{ movieData.runtime }}분</div> |
                <div class="me-1">개봉일: {{ movieData.release_date }}</div> |
                <div><v-chip color="primary" text-color="white" class="mx-2">{{ movieData.status }}</v-chip></div>
              </div>
              <!-- 줄거리 -->
              <div>
                <h5>줄거리</h5>
                <p class="p-1">{{ movieData.overview }}</p>
              </div>
            </v-expansion-panel-content>
          </v-expansion-panel>

          <!--  트레일러 -->
          <v-expansion-panel>
            <v-expansion-panel-header>
              TRAILER
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <movie-videos :video-list="movieData.video" v-if="isVideo"></movie-videos>
              <div v-if="!isVideo" class="mt-5">예고편을 준비중입니다</div>
            </v-expansion-panel-content>
          </v-expansion-panel>

          <!--  추천 / 비슷한 영화 -->
          <v-expansion-panel>
            <v-expansion-panel-header >
              Recommendations / Similiar Movie
            </v-expansion-panel-header>
            <v-expansion-panel-content class="my-3">
              <h1>RECOMMENDATIONS</h1>
              <detail-recommend-movie-list></detail-recommend-movie-list>
              <h1>SIMILAR MOVIE</h1>
              <detail-similar-movie-list></detail-similar-movie-list>
            </v-expansion-panel-content>
          </v-expansion-panel>

          <!-- 리뷰 -->
          <v-expansion-panel>
            <v-expansion-panel-header>
             REVIEWS
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <movie-review-list></movie-review-list>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import MovieVideos from '@/components/movie/MovieVideos'
import DetailRecommendMovieList from '@/components/movie/recommend/DetailRecommendMovieList'
import DetailSimilarMovieList from '@/components/movie/recommend/DetailSimilarMovieList'
import MovieReviewList from '@/components/movie/MovieReviewList'

import { mapState } from 'vuex'
import _ from 'lodash'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'MovieDetail',
  components: {
    MovieVideos,
    DetailRecommendMovieList,
    DetailSimilarMovieList,
    MovieReviewList,
  },
  data() {
    return {
      movieData: '',
      posterPath: null,
      genres: null,
      likeState: false,
      likeCount: '',
      isVideo: false,
      rating: 0,
      panel: [0]
    }
  },
  methods: {
    getMovieDetail() {
       this.$axios({
        method: 'get',
        url: `${SERVER_URL}/movie/${this.$route.params.movieId}/detail/`, 
        headers: this.config
      })
        .then(res => {
          if (res.data.adult) {
            this.$router.push({ name: 'IsAdult'})
          }
          return res
        })
        .then(res => {
          this.movieData = res.data
          // 포스터 경로 설정 
          this.posterPath = `https://image.tmdb.org/t/p/w500${res.data.poster_path}`
          // 해당 영화 좋아요 상태
          this.likeState = res.data.liked
          // 좋아요 개수 
          this.likeCount = res.data.like_count
          // 평점 계산
          this.rating = res.data.vote_average / 2
          // 장르만 뽑아내기 
          const genres = []
          _.forEach(res.data.genres, genre => {
            genres.push(genre.name)
          })
          this.genres = genres
          // 예고편 있나요
          this.isVideo = res.data.video.length > 0 ? true : false
        })
        .catch(err => {
          console.log(err)
        })
    },
    // 좋아요
    changeLike() {
      if (this.config) {
        this.$axios({
          method: 'post',
          url: `${SERVER_URL}/movie/${this.movieData.movie_id}/like/`, 
          headers: this.config
        })
          .then(() => {
            if (this.likeState) {
              this.likeCount -= 1
            } else {
              this.likeCount += 1
            }
            this.likeState = !this.likeState
          })
          .catch(err => {
            console.log(err)
          })
      } else {
        this.$router.push({ name: 'Login' })
      }
    }
  },
  created() {
    this.getMovieDetail()
  },
  computed: {
    ...mapState(['config'])
  }
}
</script>

<style>
</style>
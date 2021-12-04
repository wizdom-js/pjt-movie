<template>
  <div>
  <!-- <v-slide-group class="movieLine v-slide-item--active" show-arrows active-class="success">
    <popular-movie-list></popular-movie-list>
  </v-slide-group> -->

    <!-- review -->
    <h3>회원님의 평점을 분석한 안성맞춤 추천 영화!</h3>
    <div class="d-flex justify-center movieTag">
      <div class="d-flex" v-for="(n, idx) in range2" :key="idx">
        <h5>RECOMMENDED BY YOUR REVIEW</h5><h5 class="test2 mx-2">RECOMMENDED BY YOUR REVIEW</h5>
      </div>
    </div>
    <review-movie-list class="movieLine"></review-movie-list>
    <div class="d-flex justify-center movieTag">
      <div class="d-flex" v-for="(n, idx) in range2" :key="idx">
        <h5>RECOMMENDED BY YOUR REVIEW</h5><h5 class="test2 mx-2">RECOMMENDED BY YOUR REVIEW</h5>
      </div>
    </div>

    <!-- POPULAR  -->
    <h3>전 세계인들이 시청한 인기 영화 !</h3>
    <div class="d-flex justify-center movieTag">
      <div class="d-flex" v-for="(n, idx) in range" :key="idx">
        <h5>POPULAR MOVIE</h5><h5 class="test2 mx-2">POPULAR MOVIE</h5>
      </div>
    </div>
    <popular-movie-list class="movieLine"></popular-movie-list>
    <div class="d-flex justify-center movieTag">
      <div class="d-flex" v-for="(n, idx) in range" :key="idx">
        <h5>POPULAR MOVIE</h5><h5 class="test2 mx-2">POPULAR MOVIE</h5>
      </div>
    </div>
        
    <!-- TOP RATED -->
    <h3>높은 평점을 받은 영화</h3>
    <div class="d-flex justify-center movieTag mt-3">
      <div class="d-flex" v-for="(n, idx) in range" :key="idx">
        <h5>TOP RATED MOVIE</h5><h5 class="test2 mx-2">TOP RATED MOVIE</h5>
      </div>
    </div>
      <top-rated-movie-list class="movieLine"></top-rated-movie-list>
    <div class="d-flex movieTag justify-center">
      <div class="d-flex" v-for="(n, idx) in range" :key="idx">
        <h5>TOP RATED MOVIE</h5><h5 class="test2 mx-2">TOP RATED MOVIE</h5>
      </div>
    </div>
   
    <div v-if="showRS">
      <!-- Recommended movie -->
      <h3>회원님이 좋아요를 누른 영화 중, "{{ pickForRecommendMovie.like_movie_title }}" 기반으로 추천드려요!</h3>
      <div class="d-flex justify-center movieTag mt-3">
        <div class="d-flex" v-for="(n, idx) in range2" :key="idx">
          <h5>RECOMMENDED BY LIKES</h5><h5 class="test2 mx-2">RECOMMENDED BY YOUR LIKES</h5>
        </div>
      </div>
      <recommend-movie-list class="movieLine" :pick-recommend-movie="pickForRecommendMovie"></recommend-movie-list>
      <div class="d-flex justify-center movieTag">
        <div class="d-flex" v-for="(n, idx) in range2" :key="idx">
          <h5>RECOMMENDED BY YOUR LIKES</h5><h5 class="test2 mx-2">RECOMMENDED BY YOUR LIKES</h5>
        </div>
      </div>
      <!-- similar movie -->
      <h3>회원님이 좋아요를 누른 영화 중, "{{ pickForSimilarMovie.like_movie_title }}"와 비슷한 영화들은 어때요 ?</h3>
      <div class="d-flex justify-center movieTag mt-3">
        <div class="d-flex" v-for="(n, idx) in range2" :key="idx">
          <h5>SIMILAR TO YOUR LIKES</h5><h5 class="test2 mx-2">SIMILAR TO YOUR LIKES</h5>
        </div>
      </div>
      <similar-movie-list class="movieLine" :pick-similar-movie="pickForSimilarMovie"></similar-movie-list>
      <div class="d-flex justify-center movieTag">
        <div class="d-flex" v-for="(n, idx) in range2" :key="idx">
          <h5>SIMILAR TO YOUR LIKES</h5><h5 class="test2 mx-2">SIMILAR TO YOUR LIKES</h5>
        </div>
      </div>
    </div>

    <!-- weather -->
    <h3 >{{ weather }}</h3>
    <div class="d-flex justify-center movieTag mt-3">
      <div class="d-flex" v-for="(n, idx) in range2" :key="idx">
        <h5>RECOMMENDED BY TODAY'S WEATHER</h5><h5 class="test2 mx-2">RECOMMENDED BY TODAY'S WEATHER</h5>
      </div>
    </div>
    <weather-movie-list class="movieLine" @weather-name="getWeather"></weather-movie-list>
    <div class="d-flex justify-center movieTag">
      <div class="d-flex" v-for="(n, idx) in range2" :key="idx">
        <h5>RECOMMENDED BY TODAY'S WEATHER</h5><h5 class="test2 mx-2">RECOMMENDED BY TODAY'S WEATHER</h5>
      </div>
    </div>

    <!-- time -->
    <h3>현재 시간대에 어울리는 영화를 골라봤어요 !</h3>
    <div class="d-flex justify-center movieTag mt-3">
      <div class="d-flex" v-for="(n, idx) in range2" :key="idx">
        <h5>SUITABLE FOR THIS TIME</h5><h5 class="test2 mx-2">SUITABLE FOR THIS TIME</h5>
      </div>
    </div>
    <time-movie-list class="movieLine"></time-movie-list>
    <div class="d-flex justify-center movieTag">
      <div class="d-flex" v-for="(n, idx) in range2" :key="idx">
        <h5>SUITABLE FOR THIS TIME</h5><h5 class="test2 mx-2">SUITABLE FOR THIS TIME</h5>
      </div>
    </div>
  </div>
</template>

<script>
import PopularMovieList from '@/components/movie/recommend/PopularMovieList'
import TopRatedMovieList from '@/components/movie/recommend/TopRatedMovieList'
import RecommendMovieList from '@/components/movie/recommend/RecommendMovieList'
import SimilarMovieList from '@/components/movie/recommend/SimilarMovieList'
import WeatherMovieList from '@/components/movie/recommend/WeatherMovieList'
import TimeMovieList from '@/components/movie/recommend/TimeMovieList'
import ReviewMovieList from '@/components/movie/recommend/ReviewMovieList'
import { mapState } from 'vuex'

import _ from 'lodash'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'Recommend',
  components: {
    PopularMovieList,
    TopRatedMovieList,
    RecommendMovieList,
    SimilarMovieList,
    WeatherMovieList,
    TimeMovieList,
    ReviewMovieList,
  },
  data() {
    return {
      pickForRecommendMovie: null,
      pickForSimilarMovie: null,
      showRS: false,
      range: 4,
      range2: 2,
      weather: null,
      isRendering: false
    }
  },
  methods:{
    // 좋아요한 영화 받아오기 
    getWeather(data) {
      if (data === 'Clouds') {
        this.weather = '오늘처럼 구른 낀 날엔 이런 영화가 최고죠.'
      } else if (data === 'Drizzle') {
        this.weather = '보슬비가 내리는 지금 이 영화가 땡기지 않나요 ?'
      } else if (data === 'Rain') {
        this.weather = '비오는 날 이불속에서 보기좋은 영화들이에요 !'
      } else if (data === 'Snow') {
        this.weather = '와 눈이다! 이 영화는 어떠세요?'
      } else if (data === 'Atmosphere') {
        this.weather = '대기가 좋지않아요 ! 집 밖에 나가지 말고 영화나 보세요 !'
      } else if (data === 'Clear') {
        this.weather = '좋은 날씨에 더 신나게 볼 수 있는 영화들 !'
      } else if (data === 'Thunderstorm') {
        this.weather = '천둥소리가 너무 무서워요 ! 이 영화들로 더 무서워지세요 !'
      }
    },
    getProfile() {
      this.$axios({
        method: 'get',
        url: `${SERVER_URL}/accounts/${this.userName}/`, 
      })
        .then(res => {
          // 로그인 상태 및 좋아요한 개수에 따라 추천, 비슷한 영화 보여주는거 결정 
          if (this.userName) {
            if (res.data.like_movie.length > 1) {
              const pickTwo = _.sampleSize(res.data.like_movie, 2)
              this.pickForRecommendMovie = pickTwo[0]
              this.pickForSimilarMovie = pickTwo[1]
              this.showRS = true
            } else if (res.data.like_movie.length === 1) {
              this.pickForRecommendMovie = res.data.like_movie[0]
              this.pickForSimilarMovie = res.data.like_movie[0]
              this.showRS = true
            } else {
              this.showRS = false
            }
          }
        })
        .catch(err => {
          console.log(err)
        })
    },
  },
  computed: {
    ...mapState(['userName', 'config'])
  },
  created() {
    this.getProfile()
  },
}
</script>
    

<style scoped>
.movieLine {
  border-left-style: solid;
  border-right-style: solid;
  height: 200px;
}
.movieTag {
  border-style: solid;
  box-sizing: border-box;
  background-color: black;
  overflow: hidden;
  width: 100%;
}
.movieTag2 {
  border-style: solid;
  border-top-style: none;
  box-sizing: border-box;
  margin-bottom: 0px;
}
h5 {
  margin-bottom: 0px;
  color: white;
}
.test2 {
  color: orange;
}
h3 {
  margin-top: 30px;
}
</style>
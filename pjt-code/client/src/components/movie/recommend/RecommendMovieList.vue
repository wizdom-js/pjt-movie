<template>
  <swiper class="swiper" :options="swiperOption">
    <swiper-slide
      v-for="recommendItem in recommendMovies"
      :key="recommendItem.id"
      :recommend-item="recommendItem"
    >
      <template>
        <div @click="goToMovieDetail(recommendItem.id)" class="d-flex flex-column align-items-center">
          <img :src="`https://image.tmdb.org/t/p/w500${recommendItem.backdrop_path}`" :alt="`${recommendItem.title} 포스터`" width="100%">
          <div>{{ recommendItem.title }}</div>
        </div>
      </template>
    </swiper-slide>
    <div class="swiper-button-prev" slot="button-prev"></div>
    <div class="swiper-button-next" slot="button-prev"></div>
  </swiper>
</template>

<script>
import { Swiper, SwiperSlide } from 'vue-awesome-swiper' 
import 'swiper/css/swiper.css'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'MovieDetailRecommend',
  components: {
    Swiper,
    SwiperSlide
  },
  props: {
    pickRecommendMovie: Object,
  },
  data() {
    return {
      recommendMovies: [],
      swiperOption: {
        slidesPerView: 5,
        loop: true,
        loopFillGroupWithBlank: true,
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev'
        },
        autoplay: {
          delay: 2500,
          disableOnInteraction: false
        },
      }
    }
  },
  methods: {
    getRecommendMovie(movieId) {
      console.log(movieId)
      this.$axios({
        method: 'get',
        url: `${SERVER_URL}/movie/${movieId}/recommend/`, 
      })
        .then(res => {
          this.recommendMovies = res.data.filter(movie => {  // 포스터 없는 영화 거르기 
            return movie.backdrop_path
          })
        })
        .catch(err => {
          console.log(err)
        })
    },
    goToMovieDetail(id) {
      this.$router.push({ name: 'MovieDetail', params: { movieId: id } })
    }
  },
  created() {
    this.getRecommendMovie(this.pickRecommendMovie.movie_id)
  },
}
</script>


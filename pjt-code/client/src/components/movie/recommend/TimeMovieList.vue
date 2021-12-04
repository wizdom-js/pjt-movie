<template>
  <swiper class="swiper" :options="swiperOption">
    <swiper-slide
      v-for="timeItem in timeMovies"
      :key="timeItem.id"
      :time-item="timeItem"
    >
      <template>
        <div @click="goToMovieDetail(timeItem.id)" class="d-flex flex-column align-items-center">
          <img :src="`https://image.tmdb.org/t/p/w500${timeItem.backdrop_path}`" :alt="`${timeItem.title} 포스터`" width="100%">
          <div>{{ timeItem.title }}</div>
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
  name: 'TimeMovieList',
  components: {
    Swiper,
    SwiperSlide
  },
  data() {
    return {
      timeMovies: [],
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
    getTimeMovies() {
      this.$axios({
        method: 'get',
        url: `${SERVER_URL}/movie/time_recommend/`, 
      })
        .then(res => {
          this.timeMovies = res.data[1].filter(movie => {  // 포스터 없는 영화 거르기 
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
      this.getTimeMovies()
  }
}
</script>

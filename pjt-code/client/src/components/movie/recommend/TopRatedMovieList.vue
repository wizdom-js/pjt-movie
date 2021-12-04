<template>
  <swiper class="swiper" :options="swiperOption">
    <swiper-slide
      v-for="topRatedItem in topRatedMovies"
      :key="topRatedItem.id"
      :top-rated-item="topRatedItem"
    >
    <template>
      <div @click="goToMovieDetail(topRatedItem.id)" class="d-flex flex-column align-items-center">
        <img :src="`https://image.tmdb.org/t/p/w500${topRatedItem.backdrop_path}`" :alt="`${topRatedItem.title} 포스터`" width="100%">
        <div>{{ topRatedItem.title }}</div>
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
  name: 'TopRatedMovieList',
  components: {
    Swiper,
    SwiperSlide
  },
  data() {
    return {
      topRatedMovies: [],
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
    getTopRatedMovies() {
      this.$axios({
        method: 'get',
        url: `${SERVER_URL}/movie/top_rated/`, 
      })
        .then(res => {
          this.topRatedMovies = res.data.filter(movie => {
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
      this.getTopRatedMovies()
      new Swiper('.mySwiper')
    }
}
</script>

<style scoped>
</style>
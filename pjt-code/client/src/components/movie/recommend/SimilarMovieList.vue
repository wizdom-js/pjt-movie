<template>
  <swiper class="swiper" :options="swiperOption">
    <swiper-slide
      v-for="similarItem in similarMovies"
      :key="similarItem.id"
      :similar-item="similarItem"
    >
    <template>
      <div @click="goToMovieDetail(similarItem.id)" class="d-flex flex-column align-items-center">
        <img :src="`https://image.tmdb.org/t/p/w500${similarItem.backdrop_path}`" :alt="`${similarItem.title} 포스터`" width="100%">
        <p>{{ similarItem.title }}</p>
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
  name: 'SimilarMovieList',
  components: {
    Swiper,
    SwiperSlide
  },
  props: {
    pickSimilarMovie: Object,
  },
  data() {
    return {
      similarMovies: [],
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
    getSimilarMovie(movieId) {
      this.$axios({
        method: 'get',
        url: `${SERVER_URL}/movie/${movieId}/similar/`, 
      })
        .then(res => {
          this.similarMovies = res.data.filter(movie => {  // 포스터 없는 영화 거르기 
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
    this.getSimilarMovie(this.pickSimilarMovie.movie_id)
  },
}
</script>

<template>
  <swiper class="swiper" :options="swiperOption">
    <swiper-slide
      v-for="popularItem in popularMovie"
      :key="popularItem.id"
      :popular-item="popularItem"
    >
    <template>
      <div @click="goToMovieDetail(popularItem.id)" class="d-flex flex-column align-items-center">
        <img :src="`https://image.tmdb.org/t/p/w500${popularItem.backdrop_path}`" :alt="`${popularItem.title} 포스터`" width="100%">
        <div>{{ popularItem.title }}</div>
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
  name: 'PopularMovieList',
  components: {
    Swiper,
    SwiperSlide
  },
  data() {
    return {
      popularMovie: [],
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
    getPopularMovie() {
      this.$axios({
        method: 'get',
        url: `${SERVER_URL}/movie/popular/`, 
      })
        .then(res => {
          this.popularMovie = res.data.filter(movie => {  // 포스터 없는 영화 거르기 
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
      this.getPopularMovie()
    },
}

</script>

<style lang="scss">
.swiper-slide {
  border-right-style: solid;

}
// .turn {
//   writing-mode: vertical-rl;
//     border-left-style: solid;
/* }
.swiper-slide {
  border-left-style: solid;
} */
/* .swiper:not(:hover){
  animation:text-scroll 35s linear infinite;
}
@keyframes text-scroll{
  from{
    transform:translateX(20%);
    -moz-transform:translateX(20%);
    -webkit-transform:translateX(20%);
    -o-transform:translateX(20%);
    -ms-transform:translateX(20%);
  }
  to{
    transform:translateX(-100%);
    -moz-transform:translateX(-100%);
    -webkit-transform:translateX(-100%);
    -o-transform:translateX(-100%);
    -ms-transform:translateX(-100%);
  } */

</style>
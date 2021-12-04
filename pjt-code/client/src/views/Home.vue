<template>
  <v-row>
    <v-col cols="4" class="img">
      <img :src="require('@/assets/bg_event_hb.jpeg')" alt="" width="100%" class="img"> 
    </v-col>
    <v-col cols="8">
      <div class="my-16">
        <h3 class="notosans">현재 상영중</h3>
        <now-movie-list></now-movie-list>
      </div>
      <div class="my-16">
        <h3 class="notosans">상영 예정작</h3>
        <upcoming-movie-list></upcoming-movie-list>
      </div>
    </v-col>
  </v-row>
</template>

<script>
import NowMovieList from '@/components/movie/recommend/NowMovieList'
import UpcomingMovieList from '@/components/movie/recommend/UpcomingMovieList'

export default {
  name: 'Home',
  components: {
    NowMovieList,
    UpcomingMovieList,
  },
  data() { 
    return { 
      range: 30,
  }
}
}
</script>

<style lang="scss" scoped> 
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@500&display=swap');
.notosans {
  font-family: 'Noto Sans KR', sans-serif;
}
.film {
  background-color: black;
  height: 33px;
  
}
.whiteBox {
  width: 13px;
  height: 13px;
  background-color: white;
}
.img {
  z-index: 90 !important;
}
</style>


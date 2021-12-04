<template>
  <v-card @click="goToMovieDetail" class="m-1 d-flex flex-column justify-start align-items-center">
    <img :src="posterPath" :alt="`${recommendItem.title} 포스터`" class="cardPost">
    <p>{{ recommendItem.title }}</p>
  </v-card>
</template>

<script>
export default {
  name: 'RecommendMovieItem',
  data() {
    return {
      posterPath: `https://image.tmdb.org/t/p/w500${this.recommendItem.poster_path}`
    }
  },
  props: {
    recommendItem: Object
  },
  methods: {
    goToMovieDetail() {
      this.$router.push({ name: 'MovieDetail', params: { movieId: this.recommendItem.id } })
    }
  },
  created() {
    if (this.$route.name === 'MovieRecommend') { // 영화 추천 페이지에서 접근 했을때 
      this.posterPath = `https://image.tmdb.org/t/p/w500${this.recommendItem.backdrop_path}`
    }
  }
}
</script>

<style scoped>
.v-card {
  height: 250px;
}
.cardPost {
  height: 80%;
}
</style>
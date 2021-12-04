<template>
  <v-card @click="goToMovie()">
    <img :src="posterPath" :alt="`${movie.like_movie_title} 포스터`" width="100%" height="260px">
    <p class="text-center pt-2">{{ movie.like_movie_title }}</p>
  </v-card>
</template>

<script>
export default {
  name: 'LikeMovieItem',
  props: {
    movie: Object,
  },
  data() {
    return {
      posterPath: `https://image.tmdb.org/t/p/w500${this.movie.like_poster_path}`
    }
  },
  methods: {
    goToMovie() {
      this.$router.push({ name: 'MovieDetail', params: { movieId: this.movie.movie_id } })
    }
  }
}
</script>

<style scoped>
.v-card {
  height: 320px;
  width: 90%;
}
</style>
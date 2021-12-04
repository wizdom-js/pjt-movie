<template>
  <v-card class="d-flex flex-column align-items-center " @click="goToMovieDetail">
    <img :src="isPoster()" :alt="`${ movie.title } 포스터`"  width="100%" height="85%">
    <h3 class="mt-2">{{ movie.title }}</h3>
  </v-card>
</template>

<script>
export default {
  name: 'SearchMovieItem',
  props: {
    movie: Object
  },
  methods: {
    goToMovieDetail() {
      this.$router.push({ name: 'MovieDetail', params: { movieId: this.movie.id } })
    },
    isPoster() {
      if (this.movie.poster_path === null) {
        return require('@/assets/noimage.gif')
      } else {
        return `https://image.tmdb.org/t/p/w500${this.movie.poster_path}`
      }
    }
  }
}
</script>

<style scoped>
.v-card {
  height: 500px;
  width: 300px;
}
</style>
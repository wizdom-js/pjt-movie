<template>
  <v-card @click="goToMovieDetail" class="m-1 d-flex flex-column justify-start align-items-center">
    <img :src="posterPath" :alt="`${similarItem.title} 포스터`" class="cardPost">
    <p>{{ similarItem.title }}</p>
  </v-card>
</template>

<script>
export default {
  name: 'SimilarMovieItem',
  props: {
    similarItem: Object
  },
  data() {
    return {
      posterPath: `https://image.tmdb.org/t/p/w500${this.similarItem.poster_path}`
    }
  },
  methods: {
    goToMovieDetail() {
      this.$router.push({ name: 'MovieDetail', params: { movieId: this.similarItem.id } })
    }
  },
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
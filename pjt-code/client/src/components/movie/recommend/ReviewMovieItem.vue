<template>
  <div>
    <div @click="goToMovieDetail" class="movieitem">
      <img :src="posterPath" :alt="`${reviewItem.title} 포스터`" height="90%">
      <p>{{ reviewItem.title }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReviewMovieItem',
  data() {
    return {
      posterPath: `https://image.tmdb.org/t/p/w500${this.reviewItem.poster_path}`
    }
  },
  props: {
    reviewItem: Object
  },
  methods: {
    goToMovieDetail() {
      this.$router.push({ name: 'MovieDetail', params: { movieId: this.reviewItem.movie_id } })
    }
  }
}
</script>

<style>

</style>
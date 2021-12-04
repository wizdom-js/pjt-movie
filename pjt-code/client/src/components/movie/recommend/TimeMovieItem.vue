<template>
  <div>
    <div @click="goToMovieDetail" class="movieitem">
      <img :src="posterPath" :alt="`${timeItem.title} 포스터`" height="90%">
      <p>{{ timeItem.title }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TimeMovieItem',
  data() {
    return {
      posterPath: `https://image.tmdb.org/t/p/w500${this.timeItem.backdrop_path}`
    }
  },
  props: {
    timeItem: Object
  },
  methods: {
    goToMovieDetail() {
      this.$router.push({ name: 'MovieDetail', params: { movieId: this.timeItem.id } })
    }
  }
  

}
</script>

<style>

</style>
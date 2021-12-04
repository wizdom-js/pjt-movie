<template>
  <v-container>
    <v-row class="d-flex">
      <h5 v-if="likeCount()" class="text-center">좋아요한 영화가 없습니다.</h5>
      <v-col v-for="movie in likeMovies" :key=movie.movie_id cols="4">
        <like-movie-item :movie="movie"></like-movie-item>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import LikeMovieItem from '@/components/accounts/like/LikeMovieItem'

export default {
  name: 'LikeMovieList',
  components: {
    LikeMovieItem,
  },
  props: {
    likeMovies: Array,
  },
  methods: {
    likeCount() {
      return this.likeMovies.length < 1 ? true : false
    }
  }
}
</script>

<style>

</style>
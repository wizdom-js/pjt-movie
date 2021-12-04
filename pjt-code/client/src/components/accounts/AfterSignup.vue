<template>
  <div class="d-flex flex-column justify-center align-items-center">
    <h1>좋아하는 영화를 선택해주세요</h1>
    <v-row v-for="(genre, idx) in movies" :key="idx" class="ps-5 my-3 d-flex">
      <v-col v-for="(movie, idx) in genre" :key="idx" class="mx-2" cols="2">
        <signup-movie-item :movie="movie" @likeCountMinus="likeCountMinus" @likeCountPlus="likeCountPlus"></signup-movie-item>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import SignupMovieItem from '@/components/accounts/SignupMovieItem'

export default {
  name: 'AfterSignup',
  components: {
    SignupMovieItem
  },
  props: {
    movies: Array,
  },
  methods:{
    likeCountMinus() {
      this.$emit('likeCountMinus')
    },
    likeCountPlus() {
      this.$emit('likeCountPlus')
    }
  }
}

</script>

<style>
</style>
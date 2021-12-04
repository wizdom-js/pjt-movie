<template>
  <div class="d-flex">
    <now-movie-item
      v-for="nowItem in nowMovies"
      :key="nowItem.id"
      :now-item="nowItem"
    ></now-movie-item>
  </div>
</template>


<script>
import NowMovieItem from '@/components/movie/recommend/NowMovieItem'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'NowMovieList',
  components: {
    NowMovieItem
  },
  data() {
    return {
      nowMovies: [],
    }
  },
  methods: {
    getNowMovies() {
      this.$axios({
        method: 'get',
        url: `${SERVER_URL}/movie/now_playing/`, 
      })
        .then(res => {
          this.nowMovies = res.data.filter(movie => {  // 포스터 없는 영화 거르기 
            return movie.poster_path
          })
        })
        .catch(err => {
          console.log(err)
        })
    },
  },
  created() {
      this.getNowMovies()
    }
}
</script>

<style>

</style>
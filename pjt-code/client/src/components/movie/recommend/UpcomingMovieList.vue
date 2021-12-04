<template >
  <div class="d-flex">
    <upcoming-movie-item
      v-for="upcomingItem in upcomingMovies"
      :key="upcomingItem.id"
      :upcoming-item="upcomingItem"
    ></upcoming-movie-item>
  </div>
</template>

<script>
import UpcomingMovieItem from '@/components/movie/recommend/UpcomingMovieItem'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'UpcomingMovieList',
  components: {
    UpcomingMovieItem
  },
  data() {
    return {
      upcomingMovies: [],
    }
  },
  methods: {
    getUpcomingMovies() {
      this.$axios({
        method: 'get',
        url: `${SERVER_URL}/movie/upcoming/`, 
      })
        .then(res => {
          this.upcomingMovies = res.data.filter(movie => {  // 포스터 없는 영화 거르기 
            return movie.poster_path
          })
        })
        .catch(err => {
          console.log(err)
        })
    },
  },
  created() {
      this.getUpcomingMovies()
    }
}
</script>

<style scoped>

</style>
<template>
  <div class="overflow-x-auto d-flex recommend">
    <recommend-movie-item
      v-for="recommendItem in recommendMovies"
      :key="recommendItem.id"
      :recommend-item="recommendItem"
    ></recommend-movie-item>
  </div>
</template>

<script>
import RecommendMovieItem from '@/components/movie/recommend/RecommendMovieItem'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'DetailRecommendMovieList',
  components: {
    RecommendMovieItem
  },
  data() {
    return {
      recommendMovies: [],
    }
  },
  methods: {
    getRecommendMovie(movieId) {
      this.$axios({
        method: 'get',
        url: `${SERVER_URL}/movie/${movieId}/recommend/`, 
      })
        .then(res => {
          this.recommendMovies = res.data.filter(movie => {  // 포스터 없는 영화 거르기 
            return movie.poster_path
          })
        })
        .catch(err => {
          console.log(err)
        })
    },
  },
  created() {
    this.getRecommendMovie(this.$route.params.movieId)
  }
}
</script>

<style scoped>
.recommend {
  height: 250px;
}
</style>
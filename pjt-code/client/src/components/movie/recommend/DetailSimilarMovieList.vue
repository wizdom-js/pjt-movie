<template>
  <div>
    <div class="overflow-x-auto d-flex recommend">
      <similar-movie-item
        v-for="similarItem in similarMovies"
        :key="similarItem.id"
        :similar-item="similarItem"
      ></similar-movie-item>
    </div>
  </div>
</template>

<script>
import SimilarMovieItem from '@/components/movie/recommend/SimilarMovieItem'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'DetailSimilarMovieList',
  components: {
    SimilarMovieItem
  },
  data() {
    return {
      similarMovies: [],
    }
  },
  methods: {
    getSimilarMovie(movieId) {
      this.$axios({
        method: 'get',
        url: `${SERVER_URL}/movie/${movieId}/similar/`, 
      })
        .then(res => {
          this.similarMovies = res.data.filter(movie => {  // 포스터 없는 영화 거르기 
            return movie.poster_path
          })
        })
        .catch(err => {
          console.log(err)
        })
    },
  },
  created() { 
    this.getSimilarMovie(this.$route.params.movieId)
  },
}
</script>

<style scoped>
.recommend {
  height: 250px;
}
</style>
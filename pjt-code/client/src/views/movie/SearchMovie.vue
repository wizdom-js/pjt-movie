<template>
  <div class="notosans">
    <h1 class="d-flex flex-column justify-center align-items-center my-3">"{{ this.$route.params.keyword }}" 검색 결과</h1>
    <v-container>
      <v-row v-if="searchResult">
        <v-col v-for="movie in searchResult" :key="movie.id"
          cols="3"
        >
        <search-movie-item :movie="movie"
        ></search-movie-item>
        </v-col>
      </v-row>
      <div v-else>
        <h1>검색 결과가 없습니다.</h1>
      </div>
    </v-container>
  </div>
</template>

<script>
import SearchMovieItem from '@/components/movie/SearchMovieItem'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'Search',
  components:{
    SearchMovieItem,
  },
  data() {
    return {
      keyword: this.$route.params.keyword,
      searchResult: null,
    }
  },
  methods: {
    search() {
      this.$axios({
        method: 'get',
          url: `${SERVER_URL}/movie/${this.$route.params.keyword}/search/`,
       })
        .then(res => {
          this.searchResult = res.data.length > 0 ? res.data : false
          console.log(res.data)
        })
        .catch(err => {
          console.log(err)
        })
    }
  },
  created() {
    this.search()
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@500&display=swap');
.notosans {
  font-family: 'Noto Sans KR', sans-serif;
}
</style>
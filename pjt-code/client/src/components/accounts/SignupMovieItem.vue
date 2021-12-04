<template>
  <v-card @click="changeLike" class="d-flex flex-column align-center">
    <div>
    <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" width="100%"> 
    <p class="text-center">{{ movie.title }}</p>
    </div>
    <v-fade-transition>
      <v-overlay v-if="likeState" class="text-center" absolute>
       <v-icon color="red" x-large>mdi-heart</v-icon>
      </v-overlay>
    </v-fade-transition>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'
const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
 name: 'SignupMovieItem',
 data() {
   return {
     likeState: false
   }
 },
 props: {
   movie: Object,
 },
 methods: {
    changeLike() {
      this.$axios({
        method: 'post',
        url: `${SERVER_URL}/movie/${this.movie.movie_id}/like/`, 
        headers: this.config
      })
        .then(() => {
          if (this.likeState) {
            this.$emit('likeCountMinus')
          } else {
            this.$emit('likeCountPlus')
          }
          this.likeState = !this.likeState
        })
        .catch(err => {
          console.log(err)
        })
    }
 },
 computed: {
   ...mapState(['config']),
  }
}
</script>

<style scoped>
.v-card {
  height: 250px;
  width: 400px;
}
</style>
<template>
  <div class="d-flex flex-column">
    <div class="d-flex align-items-center">
      <v-rating v-model="rank"
        color="warning" background-color="grey"
        hover large
      ></v-rating>
      <div class="mx-3 text-h5">{{ rank }}</div>
    </div>
    <v-checkbox value="True" v-model="isSpoiler" label="스포일러를 포함한 내용인가요?"></v-checkbox>
    <div class="d-flex align-items-end">
      <v-text-field v-model.trim="review" @keyup.enter="createReview()"
        outlined placeholder="감상평을 남겨주세요."
      ></v-text-field>
      <v-btn @click="createReview()" outlined class="mx-3">등록</v-btn>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import swal from 'sweetalert'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'MovieReviewCreate',
  data() {
    return {
      review: '',
      rank: 0,
      isSpoiler: false,
    }
  },
  props: {
    reloadReview: Function,
    movieId: Number
  },
  methods: {
    createReview() {
      if (this.review === '') {
          swal ("내용을 입력하세요.", {
          dangerMode: true,
        })
      }
      const reviewItem = {
        content: this.review,
        rank: this.rank,
        is_spoiler: this.isSpoiler ? true : false,
      }
      console.log(this.is_spoiler)
      if (this.config) {
        this.$axios({
          method: 'post',
          url: `${SERVER_URL}/movie/${this.$route.params.movieId}/review_create/`,
          data: reviewItem,
          headers: this.config
        })
          .then(() => {
            this.reloadReview()
            this.review = null
            this.rank = 0
            this.isSpoiler = false
          })
          .catch(err => {
            console.log(err)
          })
      } else {
        this.$router.push({ name: 'Login' })
      }
    }
  },
  computed: {
    ...mapState(['config'])
  }
}
</script>

<style scoped>
::v-deep .v-text-field__details {
  display: none;
}
</style>
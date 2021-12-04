<template>
  <v-container>
    <movie-review-create :reload-review="getMovieReview" class="my-3"></movie-review-create>
      <h3>관람객 평점</h3>
    <div v-if="reviewList" class="overflow-y-auto reviewBlock">
      <movie-review-item 
        v-for="review in reviewList"
        :key="review.id"
        :old-review="review"
        :reload-review="getMovieReview"
      ></movie-review-item>
    </div>
    <div v-else>
      작성된 리뷰가 없습니다. 첫번째로 리뷰를 남겨보세요 ! 
    </div>
  </v-container>
</template>

<script>
import MovieReviewCreate from '@/components/movie/MovieReviewCreate'
import MovieReviewItem from '@/components/movie/MovieReviewItem'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'MovieReviewList',
  components: {
    MovieReviewItem,
    MovieReviewCreate
  },
  data() {
    return {
      reviewList: [],
    }
  },
  methods: {
    // 전체 리뷰 받아오기 
    getMovieReview() {
      this.$axios({
        method: 'get',
        url: `${SERVER_URL}/movie/${this.$route.params.movieId}/review_list/`, 
        params: {page: this.currentPage}
      })
        .then(res => {
          this.reviewList = res.data.length > 0 ? res.data : false
        })
        .catch(err => {
          console.log(err)
        })
    }, 
  },
  created() {
    this.getMovieReview()
  }
}
</script>

<style>
.reviewBlock {
  height: 700px;
}
</style>
<template>
  <v-container>
    <h5 v-if="historyCount()" class="text-center">작성한 관람평이 없습니다.</h5>
    <v-list dense>
      <v-list-item-group >
      <v-list-item v-for="(review, idx) in reviewSet" :key="review.id">
        <my-review-item :review="review" :idx="idx+1"
        ></my-review-item>
      </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-container>
</template>

<script>
import MyReviewItem from '@/components/accounts/my/MyReviewItem'

export default {
  name: 'MyReviewList',
  components: {
    MyReviewItem
  },
  props: {
    reviewSet: Array,
    reviewCount: Number
  },
  methods: {
    historyCount() {
      return this.reviewCount < 1 ? true : false
    }
  }
}
</script>

<style>

</style>
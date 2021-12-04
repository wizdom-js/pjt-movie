<template>
  <div @click="goToPost()" class="m-3 d-flex justify-space-between align-items-center">
    <p class="px-1">{{ idx }}.</p>
    <p>{{ post.title }}</p>
    <p class="date">{{ changeDate(post.created_at) }}</p>
  </div>
</template>

<script>
import _ from 'lodash'

export default {
  name: 'MyPostItem',
  props: {
    post: Object,
    idx: Number,
  },
  methods: {
    goToPost() {
      this.$router.push({ name: 'PostDetail', params: { postNum: this.post.id } })
    },
    // 날짜 슬라이싱 
    changeDate(date) {
      return _.join(_.slice(date, 0, 10), '')
    },
  }
}
</script>

<style>
.date {
  margin-left: 300px;
}
</style>
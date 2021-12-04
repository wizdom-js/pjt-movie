<template>
  <div @click="goToPost" class="m-3 d-flex">
    <p class="px-1">{{ idx }}.</p>
    <p>{{ post.title }}</p>
  </div>
</template>

<script>
export default {
  name: 'LikePostItem',
  props: {
    post: Object,
    idx: Number
  },
  methods: {
    goToPost() {
      this.$router.push({ name: 'PostDetail', params: { postNum: this.post.id } })
    }
  }

}
</script>

<style>

</style>
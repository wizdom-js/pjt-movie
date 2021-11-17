<template>
  <div>
    <h1>{{ title }}</h1>
    {{ content }}
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'PostDetail',
  computed: {
    ...mapState(['posts'])
  },
  data() {
    return {
      title: null,
      content: null,
    }
  },
  created() {
    const postItem = this.posts.filter(postDetail => {
      return postDetail.id === Number(this.$route.params.postNum)
    })[0]
    this.title = postItem.title
    this.content = postItem.content
  }
}
</script>

<style>

</style>
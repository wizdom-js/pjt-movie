<template>
  <div>
    <h1>PostList</h1>
    <div
      v-for="(post, idx) in posts"
      :key="idx"
    >
      <h1 @click="postDetail(post.id)">{{ post.title }}
      </h1>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PostList',
  data() {
    return {
      posts: null,
    }
  },
  computed: {
    getPostItem() {
      return this.$store.state.posts
    }
  },
  methods: {
    postDetail(id) {
      this.$router.push({ name: 'PostDetail', params: { postNum: id } })
    },
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`
      }
      return config
    },
    getPosts() {
      axios({
        method: 'get',
        url: `${SERVER_URL}/community/`,
        headers: this.setToken()
      })
        .then(res => {
          this.posts = res.data
        })
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>

<style>

</style>
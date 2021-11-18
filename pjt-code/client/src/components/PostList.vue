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
import { mapState } from 'vuex'
import { mapActions } from 'vuex'

export default {
  name: 'PostList',
  computed: {
    // 전체 게시글 가져오기 
    ...mapState(['posts'])
  },
  methods: {
    // 클릭한 게시글로 이동 
    postDetail(id) {
      this.$router.push({ name: 'PostDetail', params: { postNum: id } })
    },
    // 전체 게시글 서버에서 불러오기 
    ...mapActions(['getPosts'])
  },
  created() {
    this.getPosts()
  }
}
</script>

<style>

</style>
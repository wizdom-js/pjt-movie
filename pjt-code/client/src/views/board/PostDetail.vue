<template>
  <div>
    <h1>{{ post.title }}</h1>
    {{ post.content }}
    <p>마지막 수정일 :{{ post.updated_at }}</p>
    <p>작성일 : {{ post.created_at }}</p>

    <div v-if="isSameUser">
      <button @click="updatePost">update</button> |
      <button @click="deletePost">delete</button>
    </div>
    <h3>-----댓글-----</h3>
    <comment-list :comments="post.comment_set"></comment-list>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import CommentList from '@/components/CommentList'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'PostDetail',
  components: {
    CommentList
  },
  data() {
    return {
      post: null,
      isSameUser: false,
    }
  },
  computed: {
    getCommentList() {
      return this.post.comment_set
    },
    ...mapState([
      'userName',
      'config'
    ])
  },
  methods: {
    // 게시글 가져오기 
    getPost() {
      this.$axios({
        method: 'get',
        url: `${SERVER_URL}/community/${this.$route.params.postNum}/`, 
      })
        .then(res => {
          this.post = res.data
          // 지금 로그인한 유저가 글쓴 유저인지 
          if (this.userName === res.data.user.username) {
            this.isSameUser = true
          }
        })
        .catch(err => {
          console.log(err)
        })
    },
    // 게시글 삭제 
    deletePost() {
      this.$axios({
        method: 'delete',
        url: `${SERVER_URL}/community/${this.$route.params.postNum}/`, 
        headers: this.config
      })
        .then(() => {
          this.$router.push({ name: 'Board' })
        })
        .catch(err => {
          console.log(err)
        })
    },
    // 게시글 수정
    updatePost() {
      this.$router.push({ name: 'PostCreate', params: { postId: this.$route.params.postNum } })
    },

  },
  created() {
    this.getPost() // 영화 디테일 불러오기  
  }
}
</script>

<style>

</style>
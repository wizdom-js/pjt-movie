<template>
  <div>
    created
    <v-text-field v-model="post.title"
      placeholder="제목을 입력해주세요."
      color="error"
    ></v-text-field>
    <v-textarea v-model="post.content"
      color="success"
    ></v-textarea>
    <button @click="isUpdate ? updatePost() : createPost()">done</button>
  </div>
</template>

<script>
import { mapState } from 'vuex'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'PostCreate',
  data() {
    return {
      post: {
        title: '',
        content: '',
      },
      isUpdate: this.$route.params.postId > 0 ? true : false,
    }
  },
  computed: {
    ...mapState([
      'config'
    ])
  },
  created() {
    if (this.$route.params.postId > 0) {
      this.$axios({
        method: 'get',
        url: `${SERVER_URL}/community/${this.$route.params.postId}/`, 
      })
        .then(res => {
          this.post.title = res.data.title
          this.post.content = res.data.content
        })
        .catch(err => {
          console.log(err)
        })
    }
  },
  methods: {
    // 게시글 생성 
    createPost() {
      this.$axios({
        method: 'post',
        url: `${SERVER_URL}/community/`,
        data: this.post,
        headers: this.config
      })
        .then(res => {
          this.$router.push({ name: 'PostDetail', params: { postNum: res.data.id } })  
        })
        .catch(err => {
          console.log(err)
        })
    },
    // 게시글 수정
    updatePost() {
      this.$axios({
        method: 'put',
        url: `${SERVER_URL}/community/${this.$route.params.postId}/`, 
        data: this.post,
        headers: this.config
      })
        .then(res => {
          this.$router.push({ name: 'PostDetail', params: { postNum: res.data.id } })  
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
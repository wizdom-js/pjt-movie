<template>
  <div>
    <h2 v-if="isUpdate" class="d-flex justify-center mt-5">게시글 수정</h2>
    <h2 v-else class="d-flex justify-center mt-5">게시글 작성</h2>
    <v-container>
    <p>제목</p>
      <v-text-field v-model.trim="post.title"
      solo
      placeholder="제목을 입력해주세요."
      color="error"
    ></v-text-field>
    <p>내용</p>
    <v-textarea
      auto-grow
      solo
      v-model.trim="post.content"
      placeholder="내용을 입력해주세요."
    ></v-textarea>
      <v-btn
      elevation="1"
      large
      outlined
      rounded
      @click="isUpdate ? updatePost() : createPost()"
      style="float:right"
    >DONE</v-btn>
    </v-container>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import swal from 'sweetalert'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'PostCreate',
  data() {
    return {
      post: {
        title: '',
        content: '',
        id: '',
      },
      isUpdate: null,
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
        url: `${SERVER_URL}/community/${this.$route.params.postId}/detail/`, 
      })
        .then(res => {
          this.post.title = res.data.title
          this.post.content = res.data.content
          this.post.id = res.data.id
          this.isUpdate = res.data.id > 0 ? true : false
        })
        .catch(err => {
          console.log(err)
        })
    }
  },
  methods: {
    // 게시글 생성 
    createPost() {
      if (this.post.title === '') {
          swal ("제목을 입력해주세요.", {
          dangerMode: true,
        })
      } else if (this.post.content === '') {
          swal ("내용을 입력해주세요.", {
          dangerMode: true,
        })
      }
      this.$axios({
        method: 'post',
        url: `${SERVER_URL}/community/post/`,
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
        url: `${SERVER_URL}/community/${this.post.id}/`, 
        data: this.post,
        headers: this.config
      })
        .then(() => {
          this.$router.push({ name: 'PostDetail', params: { postNum: this.post.id } })  
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
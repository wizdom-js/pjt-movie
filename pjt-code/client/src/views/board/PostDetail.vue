<template>
  <v-container>
    <div class="d-flex justify-space-between align-items-start">
      <!-- 헤더 -->
      <div>
      <h1>{{ post.title }}</h1>
      <div class="d-flex mx-2 align-items-end" @click="goToUserProfile()">
        <div class="me-3">작성자: </div>
        <img :src="getUserProfileImg(post.user.profile_image)" class="profileImg">
        <div class="ms-2">{{ post.user.nickname }}</div>
      </div>
      </div>
      <div class="d-flex flex-column align-items-end">
        <p>작성일: {{ changeDate(post.created_at) }}</p>
        <p>마지막 수정일: {{ changeDate(post.updated_at) }}</p>
      </div>
    </div>
    <v-divider></v-divider>
    <!-- 내용 -->
    <div v-html="content"></div>
    <!-- 좋아요 / 수정 삭제 -->
    <div class="d-flex justify-space-between align-items-end mt-10">
      <div @click="changeLike" class="d-flex align-items-end">
        <div v-if="likeState"><v-icon color="red" large>mdi-heart</v-icon>좋아요 취소</div>
        <div v-else><v-icon color="red">mdi-heart-outline</v-icon>좋아요</div>
        <div class="mx-3">{{ likeCount }}</div>
      </div>
      <div v-if="isSameUser">
        <v-btn @click="updatePost" class="mx-2" outlined color="indigo">UPDATE</v-btn>
        <v-btn @click="deletePost" outlined color="error">DELETE</v-btn>
      </div>
    </div>
    <v-divider></v-divider>
    <h5>댓글</h5>
    <comment-list :comments="post.comment_set" class="my-5"></comment-list>
  </v-container>
</template>

<script>
import { mapState } from 'vuex'
import CommentList from '@/components/CommentList'

import _ from 'lodash'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'PostDetail',
  components: {
    CommentList
  },
  data() {
    return {
      post: '',
      content: '',
      isSameUser: false,
      likeState: null,
      likeCount: null,
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
    // 게시글 정보 가져오기 
    getPost() {
      this.$axios({
        method: 'get',
        url: `${SERVER_URL}/community/${this.$route.params.postNum}/detail/`, 
        headers: this.config
      })
        .then(res => {
          this.post = res.data
          this.content = res.data.content.split('\n').join('<br />')
          // 지금 로그인한 유저가 글쓴 유저인지 
          if (this.userName === res.data.user.username) {
            this.isSameUser = true
          }
          // 좋아요 상태
          this.likeState = res.data.is_liked
          // 좋아요 개수 
          this.likeCount = res.data.likes_count
        })
        .catch(err => {
          console.log(err)
        })
    },
    // 게시글 삭제 
    deletePost() {
      this.$axios({
        method: 'delete',
        url: `${SERVER_URL}/community/${this.post.id}/`, 
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
      this.$router.push({ name: 'PostCreate', params: { postId: this.post.id } })
    },
    // 좋아요
    changeLike() {
      this.$axios({
        method: 'post',
        url: `${SERVER_URL}/community/${this.post.id}/likes/`, 
        headers: this.config
      })
        .then(() => {
          if (this.likeState) {  
            this.likeCount -= 1 // 좋아요한 상태라면
          } else {              
            this.likeCount += 1 // 좋아요한 상태 아님 
          }
          this.likeState = !this.likeState
        })
        .catch(err => {
          console.log(err)
        })
    },
    // 날짜 슬라이싱 
    changeDate(date) {
      return _.join(_.slice(date, 0, 10), '')
    },
    // 프로필 이미지
    getUserProfileImg(img) { 
      if (img === null) {
        return 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQU00i-_pNcxxQ69OH2c8MyVuHS0Q4GdMDR7w&usqp=CAU'
      } else {
        return `http://127.0.0.1:8000${img}`
      }
    },
    goToUserProfile() {
      this.$router.push({ name: 'Profile', params: { userName: this.post.user.username } })
    },
  },
  created() {
    this.getPost() // 영화 디테일 불러오기  
  }
}
</script>

<style scoped>
.profileImg {
  height: 30px;
  width: 30px;
  border-style: solid;
  border-width: 1px;
  border-radius: 100%;
}
</style>
<template>
  <div>
    <v-row v-if="!isUpdate">
      <v-col @click="goToUserProfile()" cols="1" class="text-center">
        <img :src="getUserProfileImg()" class="profileImg">
      </v-col>
      <v-col cols="8">
        <p @click="goToUserProfile()">{{ comment.user.nickname }}</p>
        <p class="my-5">{{ comment.content }}</p>
        <i>작성일: {{ changeDate(comment.created_at) }}</i>
      </v-col>
      <v-col v-if="isSameUser" cols="2" class="d-flex align-items-end justify-end">
        <v-btn @click="showInput" outlined class="udBtn">update</v-btn>
        <v-btn @click="deleteComment" plain outlined class="udBtn">delete</v-btn>
      </v-col>
    </v-row>
    <div v-else class="my-5 d-flex align-items-end">
      <v-text-field v-model.trim="field.content" @keyup.enter="updateComment()"
        outlined
        clearable
        label="댓글 수정"
      ></v-text-field>
      <div class="d-flex flex-column ">
        <v-btn @click="isUpdate = !isUpdate" outlined class="udBtn">취소</v-btn>
        <v-btn @click="updateComment" outlined class="udBtn">완료</v-btn>
      </div>
    </div>
    <v-divider class="px-10"></v-divider>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import _ from 'lodash'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'CommentItem',
  data() {
    return {
      field: {
        content: null,
      },
      isSameUser: false,
      isUpdate: false,
      profileImg: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQU00i-_pNcxxQ69OH2c8MyVuHS0Q4GdMDR7w&usqp=CAU',
    }
  },
  props: {
    comment: Object,
    reloadComment: Function
  },
  methods: {
    // 댓글 삭제 
    deleteComment() {
      this.$axios({
        method: 'delete',
        url: `${SERVER_URL}/community/${this.comment.post_id}/comment/${this.comment.id}/`, 
        headers: this.config
      })
        .then(() => {
          this.reloadComment()
        })
        .catch(err => {
          console.log(err)
        })
    },
    // 댓글 수정 
    updateComment() { 
      this.$axios({
        method: 'put',
        url: `${SERVER_URL}/community/${this.comment.post_id}/comment/${this.comment.id}/`, 
        data: this.field,
        headers: this.config
      })
        .then(() => {
          // console.log(res)
          this.reloadComment()
          this.isUpdate = !this.isUpdate
        })
        .catch(err => {
          console.log(err)
        })
    },
    // 수정 버튼 눌렸을 때, input창 나타내기 
    showInput() { 
      this.isUpdate = !this.isUpdate
      this.field.content = this.comment.content
    },
    // 프로필 이미지
    getUserProfileImg() {
      if (this.comment.user.profile_image === null) {
        return 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQU00i-_pNcxxQ69OH2c8MyVuHS0Q4GdMDR7w&usqp=CAU'
      } else {
        return `http://127.0.0.1:8000${this.comment.user.profile_image}`
      }
    },
    goToUserProfile() {
      this.$router.push({ name: 'Profile', params: { userName: this.comment.user.username } })
    },
    // 날짜 슬라이싱 
    changeDate(date) {
      return _.join(_.slice(date, 0, 10), '')
    },
  },
  created() {
    // 지금 로그인한 유저가 글쓴 유저인지 
    if (this.userName === this.comment.user.username) {
      this.isSameUser = true
    }
    // // 유저 프로필
    // if (this.comment.profile_image === null) {
    //     this.profileImg =  'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQU00i-_pNcxxQ69OH2c8MyVuHS0Q4GdMDR7w&usqp=CAU'
    // } else {
    //   this.profileImg = `http://127.0.0.1:8000${this.comment.profile_image}`
    // }
  },
  computed: {
    ...mapState(['userName', 'config'])
  },
  // watch: {
  //   comment() {
  //     this.getUserProfileImg()
  //   }
  // }
}
</script>

<style scoped>
.profileImg {
  height: 50px;
  width: 50px;
  border-style: solid;
  border-radius: 100%;
}
.udBtn {
  border-style: none;
  padding-left: 5px;
  padding-right: 5px;
}
::v-deep .v-text-field__details {
  display: none;
}
</style>
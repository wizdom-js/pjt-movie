<template>
  <div class="d-flex justify-space-between align-items-center m-3">
    <div @click="goToUserProfile()">
      <img :src="getUserProfileImg()" :alt="`${ follower.nickname }님의 프로필 사진`" class="profileImg">
      {{ follower.nickname }}
    </div>
    <!-- 프로필에 해당하는 유저라면 팔로워 삭제 버튼 보이게 하기  -->
    <button v-if="this.userName === this.$route.params.userName" @click="deleteFollower(follower.username)"
      class="me-10"
    >delete</button>
  </div>
</template>

<script>
import { mapState } from 'vuex'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'FollowerItem',
  props:{
    follower: Object
  },
  methods: {
    // 팔로우 삭제 
    deleteFollower(deleteUserName) {
      this.$axios({
        method: 'post',
        url: `${SERVER_URL}/accounts/${this.userName}/delete/${deleteUserName}/`,
        headers: this.config
      })
        .then(res => {
          this.$emit('reload-follower', res.data.followers) // 새로 받은 follower 리스트 올려주기 
        })
        .catch(err => {
          console.log(err)
        })
    },
    // 클릭한 유저 프로필로 이동
    goToUserProfile() {
      this.$router.push({ name: 'Profile', params: { userName: this.follower.username } })
    },
    // 프로필 이미지
    getUserProfileImg() {
      if (this.follower.profile_image === null) {
        return 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQU00i-_pNcxxQ69OH2c8MyVuHS0Q4GdMDR7w&usqp=CAU'
      } else {
        return `http://127.0.0.1:8000${this.follower.profile_image}`
      }
    }
  },
  computed: {
    ...mapState(['config', 'userName'])
  },
}
</script>

<style scoped>
.profileImg {
  height: 50px;
  width: 50px;
  border-style: solid;
  border-radius: 100%;
}
</style>
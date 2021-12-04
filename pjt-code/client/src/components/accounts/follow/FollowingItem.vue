<template>
  <div class="d-flex justify-space-between align-items-center m-3">
    <div @click="goToUserProfile">
      <img :src="getUserProfileImg()" :alt="`${ followingUser.nickname }님의 프로필 사진`" class="profileImg">
      {{ followingUser.nickname }}
    </div>
    <!-- 프로필에 해당하는 유저라면 팔로우 버튼 보이게하기  -->
    <div v-if="this.userName === this.$route.params.userName" class="me-10">
      <button v-if="followState" @click="followingChangeState">unfollow</button>
      <button v-else @click="followingChangeState">follow</button>
    </div>
    
  </div>
</template>

<script>
import { mapState } from 'vuex'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'FollowingItem',
  data() {
    return {
      followState: true,
    }
  },
  props: {
    followingUser: Object
  },
  methods: {
    // 팔로잉 상태 변경 
    followingChangeState() {
      this.$axios({
        method: 'post',
        url: `${SERVER_URL}/accounts/${this.followingUser.username}/follow/`,
        headers: this.config
      })
        .then(() => {
          if (this.followState) {
            this.$emit('unfollow')
            this.followState = false
          } else {
            this.$emit('follow')
            this.followState = true
          }
        })
        .catch(err => {
          console.log(err)
        })
    },
    // 클릭한 유저 프로필로 이동
    goToUserProfile() {
      this.$router.push({ name: 'Profile', params: { userName: this.followingUser.username } })
    },
    // 프로필 이미지
    getUserProfileImg() {
      if (this.followingUser.profile_image === null) {
        return 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQU00i-_pNcxxQ69OH2c8MyVuHS0Q4GdMDR7w&usqp=CAU'
      } else {
        return `http://127.0.0.1:8000${this.followingUser.profile_image}`
      }
    }
  },
  computed: {
    ...mapState(['config', 'userName'])
  },
}
</script>

<style scoped>
.hide {
  display: none;
}
.profileImg {
  height: 50px;
  width: 50px;
  border-style: solid;
  border-radius: 100%;
}
</style>
<template>
  <v-container>
    <h5 v-if="followCount()" class="text-center">팔로우하는 회원이 없습니다.</h5>
    <follower-item 
      v-for="follower in followerUsers"
      :key="follower.id"
      :follower="follower"
      @reload-follower="reloadFollower"
    ></follower-item>
  </v-container>
</template>

<script>
import FollowerItem from '@/components/accounts/follow/FollowerItem'

export default {
  name: 'FollowerList',
  components: {
    FollowerItem
  },
  data() {
    return {
      followerUsers: this.followers,
    }
  },
  props: {
    followers: Array,
    followersCount: Number
  },
  methods: {
    // 팔로워 삭제했을때 리스트 업뎃 및 숫자 감소
    reloadFollower(newFollowers) {
      this.followerUsers = newFollowers
      this.$emit('delete-follower')
    },
    followCount() {
      return this.followersCount < 1 ? true : false
    }
  }, 
  watch: {
    followers() {
      this.followerUsers = this.followers
    }
  },
}
</script>

<style>

</style> 
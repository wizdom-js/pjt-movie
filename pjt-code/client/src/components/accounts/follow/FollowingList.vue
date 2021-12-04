<template>
  <v-container>
    <h5 v-if="followCount()" class="text-center">팔로잉하는 회원이 없습니다.</h5>
    <following-item
      v-for="following in followings"
      :key="following.id"
      :following-user="following"
      @unfollow="unfollow"
      @follow="follow"
    ></following-item>
  </v-container>
</template>

<script>
import FollowingItem from '@/components/accounts/follow/FollowingItem'

export default {
  name: 'FollowingList',
  components: {
    FollowingItem
  },
  props: {
    followings: Array,
    followingsCount: Number
  },
  methods: {
    unfollow() {
      this.$emit('unfollow')
    },
    follow() {
      this.$emit('follow')
    },
    followCount() {
      return this.followingsCount < 1 ? true : false
    }
  }
}
</script>

<style>

</style>
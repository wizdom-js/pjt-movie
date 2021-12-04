<template>
 <v-container>
    <h5 v-if="historyCount()" class="text-center">작성한 게시글이 없습니다.</h5>
    <v-list dense>
      <v-list-item-group >
      <v-list-item v-for="(post, idx) in postSet" :key="post.id">
        <my-post-item :post="post" :idx="idx+1"
        ></my-post-item>
      </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-container>
</template>

<script>
import MyPostItem from '@/components/accounts/my/MyPostItem'

export default {
  name: 'MyPostList',
  components: {
    MyPostItem
  },
  props: {
    postSet: Array,
    postCount: Number
  },
  methods: {
    historyCount() {
      return this.postCount < 1 ? true : false
    }
  }
}
</script>

<style>

</style>
<template>
  <v-container>
    <h5 v-if="historyCount()" class="text-center">작성한 댓글이 없습니다.</h5>
    <v-list dense>
      <v-list-item-group >
      <v-list-item v-for="(comment, idx) in commentSet" :key="comment.id">
        <my-comment-item :comment="comment" :idx="idx+1"
        ></my-comment-item>
      </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-container>
</template>

<script>
import MyCommentItem from '@/components/accounts/my/MyCommentItem'

export default {
  name: 'MyCommentList',
  components: {
    MyCommentItem
  },
  props: {
    commentSet: Array,
    commentCount: Number
  },
  methods: {
    historyCount() {
      return this.commentCount < 1 ? true : false
    }
  }
}
</script>

<style>

</style>
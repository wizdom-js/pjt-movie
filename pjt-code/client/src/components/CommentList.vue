<template>
  <div>
    <comment-create :reloadComment="reloadComment"></comment-create>
    <comment-item
      v-for="comment in comments"
      :key="comment.id"
      :comment="comment"  
      :reloadComment="reloadComment"
    ></comment-item>
  </div>
</template>

<script>
import CommentItem from '@/components/CommentItem'
import CommentCreate from '@/components/CommentCreate'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'CommentList',
  components: {
    CommentItem,
    CommentCreate
  },
  data() {
    return {
      content: null,
      comment: null,
    }
  },
  props: {
    comments: {
      type: Array,
    }
  },
  methods: {
    reloadComment() {
      this.$axios({
        method: 'get',
        url: `${SERVER_URL}/community/${this.$route.params.postNum}/comment/`,
      })
        .then(res => {
          this.comments = res.data
        })
        .catch(err => {
          console.log(err)
        })
    },
  }
}
</script>

<style>

</style>
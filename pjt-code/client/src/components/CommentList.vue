<template>
  <div>
    <comment-create :reloadComment="reloadComment"></comment-create>
      <comment-item
        v-for="comment in commentList"
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
      commentList: this.comments
    }
  },
  props: {
    comments: {
      type: Array,
    }
  },
  methods: {
    // 댓글 다시 로드 
    reloadComment() {
      this.$axios({
        method: 'get',
        url: `${SERVER_URL}/community/${this.$route.params.postNum}/comment_list/`,
      })
        .then(res => {
          this.commentList = res.data
        })
        .catch(() => {
          // console.log(err)
          this.commentList = null
        })
    },
  },
  watch: {
    comments() {
      this.commentList = this.comments
      console.log(this.commentList)
    }
  }
}
</script>

<style>

</style>
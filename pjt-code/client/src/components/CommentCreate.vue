<template>
  <div class="d-flex align-items-end">
    <v-text-field v-model.trim="content" @keyup.enter="createComment()"
      placeholder="댓글을 작성해주세요."
      outlined
      clearable
    >
    </v-text-field>
    <v-btn @click="createComment()" outlined class="createButton">등록</v-btn>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import swal from 'sweetalert'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'CommentCreate',
  data() {
    return {
      content: '',
    }
  },
  props: {
    reloadComment: Function
  },
  methods: {
    createComment() {
      if (this.content === '') {
          swal ("댓글을 입력해주세요.", {
          dangerMode: true,
        })
      }
      const commentItem = {
        content: this.content
      }
      if (this.config) {
        this.$axios({
          method: 'post',
          url: `${SERVER_URL}/community/${this.$route.params.postNum}/comment_create/`,
          data: commentItem,
          headers: this.config
        })
          .then(() => {
            this.reloadComment()
            this.content = null
            // swal('하이')
          })
          .catch(err => {
            console.log(err)
          })
      } else {
        this.$router.push({ name: 'Login' })
      }
    }
  },
  computed: {
    ...mapState(['config'])
  }
}
</script>

<style scoped>
.createButton {
  border-style: none;
}
::v-deep .v-text-field__details {
  display: none;
}
</style>
<template>
  <div>
     <v-text-field v-model.trim="fields.content" color="error" @keyup.enter="createComment"></v-text-field>
     <button @click="createComment">+</button>
  </div>
</template>

<script>
import { mapState } from 'vuex'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'CommentCreate',
  data() {
    return {
      fields: {
         content: null,
      }
    }
  },
  props: {
    reloadComment: Function
  },
  methods: {
    createComment() {
      this.$axios({
        method: 'post',
        url: `${SERVER_URL}/community/${this.$route.params.postNum}/comment/`,
        data: this.fields,
        headers: this.config
      })
        .then(() => {
          this.reloadComment()
          this.fields.content = null
        })
        .catch(err => {
          console.log(err)
        })
    }
  },
  computed: {
    ...mapState(['config'])
  }
}
</script>

<style>

</style>
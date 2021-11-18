<template>
  <v-container>
    <post-list></post-list>
  <button @click="postCreate">Create</button>
  </v-container>
</template>

<script>
  import PostList from '@/components/PostList'

  export default {
    name: 'Board',
    components: {
      PostList,
    },
    methods: {
      postCreate() {
        const token = localStorage.getItem('jwt')
        if (token) { // 로그인 상태 -> 게시글 생성 
          this.$router.push({ name: 'PostCreate', params: { postId: 0 }})
        } else {    // 비로그인 상태 -> 로그인 
          this.$router.push({ name: 'Login' })
        }
      },
    },
  }
</script>

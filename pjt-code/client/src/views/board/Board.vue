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
        if (token) {
          this.$router.push({ name: 'PostCreate'})
        } else {
          this.$router.push({ name: 'Login' })
        }
      },
    },
  }
</script>

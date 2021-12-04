<template>
  <v-container>
    <post-list></post-list>
  </v-container>
</template>

<script>
import PostList from '@/components/PostList'

export default {
  name: 'Board',
  components: {
    PostList,
  },
}
</script>

<style scoped>

</style>
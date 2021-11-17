<template>
  <v-app>
    <nav>
      <router-link :to="{ name: 'Home' }">HOME</router-link> |
      <router-link :to="{ name: 'Board' }">Board</router-link> |
      <router-link :to="{ name: 'Recommend' }">Recommend</router-link> |
      <div v-if="isLogin">
        <router-link :to="{ name: 'User' }">User</router-link> |
        <router-link to="#" @click.native="logout">Logout</router-link>
      </div>
      <div v-else>
        <router-link :to="{ name: 'Signup' }">Signup</router-link> | 
        <router-link :to="{ name: 'Login' }">Login</router-link>
      </div>
    </nav>

    <v-main>
      <router-view @login="isLogin=true"/>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',
  data: function () {
    return {
      isLogin: false,
    }
  },
  methods: {
    logout: function() {
      this.isLogin = false
      localStorage.removeItem('jwt')
      this.$router.push({ name: 'Login' })
    }
  },
  created: function () {
    const token = localStorage.getItem('jwt')
    if (token) {
      this.isLogin = true
    }
  }
}
</script>

<template>
  <div>
    <h1>Login</h1>
    <div>
      <label for="username">사용자 이름: </label>
      <input 
        type="text" 
        id="username"
        v-model="credentials.username"
      >
    </div>
    <div>
      <label for="password">비밀번호: </label>
      <input 
        type="password" 
        id="password"
        v-model="credentials.password"
      >
    </div>
    <button @click="login">로그인</button>
  </div>
</template>

<script>
const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'Login',
  data: function () {
    return {
      credentials: {
        username: null,
        password: null,
      }
    }
  },
  methods: {
    login: function () {
      this.$axios({
        method: 'post',
        url: `${SERVER_URL}/accounts/api-token-auth/`,
        data: this.credentials,
      })
        .then(res => {
          localStorage.setItem('jwt', res.data.token)
          this.$emit('login')
          this.$router.push({ name: 'TodoList' })
        })
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>

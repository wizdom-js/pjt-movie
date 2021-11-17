<template>
  <div>
    <h1>Signup</h1>
    <div>
      <label for="username">아이디: </label>
      <input 
        type="text" 
        id="username"
        v-model="credentials.username"
      >
    </div>
    <div>
      <label for="nickname">닉네임: </label>
      <input 
        type="text" 
        id="nickname"
        v-model="credentials.nickname"
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
    <div>
      <label for="passwordConfirmation">비밀번호 확인: </label>
      <input
        type="password" 
        id="passwordConfirmation"
        v-model="credentials.passwordConfirmation"
        @keyup.enter="signup"
      >
    </div>
    <div>
      <label for="email">이메일: </label>
      <input 
        type="email" 
        id="email"
        v-model="credentials.email"
      >
    </div>
    <button @click="signup">회원가입</button>
  </div>
</template>

<script>
const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'Signup',
  data: function () {
    return {
      credentials: {
        username: null,
        nickname: null,
        password: null,
        passwordConfirmation: null,
        email: null,
      }
    }
  },
  methods: {
    signup: function () {
      this.$axios({
        method: 'post',
        url: `${SERVER_URL}/accounts/signup/`, 
        data: this.credentials,
      })
        .then(() => {
          this.$axios({
            method: 'post',
            url: `${SERVER_URL}/accounts/api-token-auth/`,
            data: this.credentials,
          })
            .then(res => {
              localStorage.setItem('jwt', res.data.token)
              this.$emit('login')
              this.$router.push({ name: 'Home' })
            })
            .catch(err => {
              console.log(err)
            })
        })
        .catch(err => {
          console.log(this.credentials)
          console.log(err)
        })
    }
  }
}
</script>
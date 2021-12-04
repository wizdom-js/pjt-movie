<template>
  <v-container class="text-center">
    <div class="loginBox">
    <h1>LOGIN</h1>
    <!-- <div>
      <label for="username">사용자 이름: </label>
      <input 
        type="text" 
        id="username"
        v-model="credentials.username"
      >
    </div> -->
    <v-text-field
      v-model="credentials.username"
      label="ID"
    ></v-text-field>

   
    <!-- <div>
      <label for="password">비밀번호: </label>
      <input 
        type="password" 
        id="password"
        v-model="credentials.password"
        @keyup.enter="login"
      >
    </div> -->
    <v-text-field
      v-model="credentials.password"
      :append-icon="credentials.show1 ? 'mdi-eye' : 'mdi-eye-off'"
      :rules="[credentials.rules.required, credentials.rules.min]"
      :type="credentials.show1 ? 'text' : 'password'"
      name="input-10-1"
      label="Password"
      @click:append="credentials.show1 = !credentials.show1"
      @keyup.enter="login"
    ></v-text-field>

    <v-btn
      elevation="1"
      outlined
      rounded
      @click="login"
    >로그인</v-btn>
    </div>
  </v-container>
</template>

<script>
const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'Login',
  data: function () {
    return {
      credentials: {
        username: null,
        show1: false,
        password: '',
        rules: {
          required: value => !!value || '비밀번호를 입력하세요.',
          min: v => v.length >= 8 || '비밀번호는 8글자 이상입니다.',
        },
      }
    }
  },
  methods: {
    login() {
      this.$axios({
        method: 'post',
        url: `${SERVER_URL}/accounts/api-token-auth/`,
        data: this.credentials,
      })
        .then(res => {
          localStorage.setItem('jwt', res.data.token) // jwt 토큰 localStorage에 저장 
          this.$store.dispatch('setUserName', this.credentials.username)  // 로그인한 유저 아이디 저장 
          this.$store.dispatch('setToken')  // 토큰 state에 저장 
        })
        .then(() => { // 유저정보 받아오기 
          this.$axios({
            method: 'get',
            url: `${SERVER_URL}/accounts/${this.credentials.username}/`, 
          })
          .then(res => {
            this.$store.dispatch('setUserProfileImg', res.data.profile_image) // 로그인한 유저 프로필 이미지 저장
            this.$store.dispatch('setIsAdmin', res.data.is_superuser) // 로그인한 유저 관리자 여부 저장
            this.$router.push({ name: 'Home' })
          })
        })
        .catch(err => {
          console.log(err)
        })
    },
  }
}
</script>

<style scoped>
.loginBox {
  height: 100px;
  width: 300px;
  margin: auto;
  margin-top: 50px;
}
</style>
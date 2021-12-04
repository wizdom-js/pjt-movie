<template>
  <v-container>
    <h1 class="text-center py-5">SIGN UP</h1>
    <v-stepper v-model="e1">
      <!-- 진행과정 -->
      <v-stepper-header>
        <v-stepper-step
          :complete="e1 > 1"
          step="1" >
          SIGN UP
        </v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step
          :complete="e1 > 2"
          step="2" >
          CHOOSE GENRES YOU LIKE
        </v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step 
          :complete="e1 > 3"
          step="3" >
          LIKE MOVIES YOU LIKE
        </v-stepper-step>
      </v-stepper-header>
      
      <v-stepper-items>
      <!-- step1 회원가입 -->
        <v-stepper-content step="1" class="paddingForm">
          <v-form ref="form" v-model="valid" lazy-validation class="text-center">
          <v-text-field
            v-model="credentials.username"
            :rules="[credentials.rules.required]"
            label="ID"
            placeholder="아이디를 입력해주세요."
            required
          ></v-text-field>

          <v-text-field
            v-model="credentials.nickname"
            :rules="[credentials.rules.required, credentials.rules.nickname]"
            label="Nickname"
            placeholder="닉네임을 입력해주세요"
          ></v-text-field>

          <v-text-field
            v-model="credentials.password"
            :append-icon="credentials.show1 ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="[credentials.rules.required, credentials.rules.min]"
            :type="credentials.show1 ? 'text' : 'password'"
            name="input-10-1"
            label="Password"
            placeholder="사용하실 비밀번호를 입력해주세요"
            @click:append="credentials.show1 = !credentials.show1"
          ></v-text-field>
          
          <v-text-field
            v-model="credentials.passwordConfirmation"
            :rules="[credentials.rules.required, credentials.rules.match]"
            :type="credentials.show2 ? 'text' : 'password'"
            name="input-10-1"
            label="Password Confirmation"
            placeholder="사용하실 비밀번호를 한번 더 입력해주세요"
            @click:append="credentials.show2 = !credentials.show2"
          ></v-text-field>

          <v-text-field
            v-model="credentials.email"
            :rules="[credentials.rules.email]"
            label="E-Mail"
            placeholder="이메일을 입력해주세요"
          ></v-text-field>
          <v-btn
            outlined
            :disabled="!valid"
            @click="validate"
            x-large
            class="mt-5"
          >SIGN UP</v-btn>
          </v-form>
      </v-stepper-content>

      <!-- 장르고르기 -->
      <v-stepper-content step="2" class="paddingForm text-center">
        <v-select
          v-model="values"
          ref="genres"
          :items="items"
          chips
          :label="`${credentials.nickname}님이 좋아하는 장르`"
          multiple
          item-text="name"
          item-value="value"
          color="deep-color"
          :rules="[() => this.values.length >= 2 || '좋아하는 장르를 2개 이상 선택해주세요.']"
        ></v-select>
        <v-btn
            outlined
            @click="validateGenre"
            x-large
          >GO TO LIKE MOVIE</v-btn>
      </v-stepper-content>
    
      <!-- 영화좋아요 -->
      <v-stepper-content step="3" class="text-center">
        <after-signup :movies="movies" @likeCountMinus="likeCountMinus" @likeCountPlus="likeCountPlus"></after-signup>
        <v-btn
          outlined
          @click="validateLike"
          x-large
          class="mt-5"
        >DONE !</v-btn>
      </v-stepper-content>
      </v-stepper-items>
    </v-stepper>
  </v-container>
</template>

<script>
import AfterSignup from '@/components/accounts/AfterSignup'
import swal from 'sweetalert';

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'Signup',
  components: {
    AfterSignup
  },
  data: function () {
    return {
      // 스텝
      e1: 1,
      // 회원가입 데이터
      valid: true,
      credentials: {                   
        username: '',
        nickname: '',
        passwordConfirmation: '',
        email: null,
        show1: false,
        show2: false,
        password: '',
        rules: {
          required: value => !!value || `필수 입력 요소입니다.`,
          min: v => v.length >= 8 || '비밀번호는 8글자 이상입니다.',
          match: passwordCom => this.credentials.password === passwordCom || '비밀번호가 일치하지 않습니다.',
          email: email => /.+@.+\..+/.test(email) || '유효한 이메일 형식이 아닙니다.',
          nickname: nickname => nickname.length <= 10 || '닉네임을 10자 이내로 설정해주세요.'
        },
      },
      // 장르선택
      values: [],
      items: [
        { name: 'SF', value: '878' },
        { name: 'TV 영화', value: '10770' },
        { name: '가족', value: '10751' },
        { name: '공포', value: '27' },
        { name: '드라마', value: '18' },
        { name: '로맨스', value: '10749' },
        { name: '모험', value: '12' },
        { name: '미스터리', value: '9648' },
        { name: '범죄', value: '80' },
        { name: '서부', value: '37' },
        { name: '스릴러', value: '53' },
        { name: '애니메이션', value: '16' },
        { name: '액션', value: '28' },
        { name: '역사', value: '36' },
        { name: '음악', value: '10402' },
        { name: '판타지', value: '14' },
        { name: '전쟁', value: '10752' },
        { name: '코미디', value: '35' },
      ],
      // 영화 선택
      movies: [],
      likeCount: 0,
    }
  },
  methods: {
    // 회원가입 
    signup() {
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
              this.$store.dispatch('setUserName', this.credentials.username)  // 로그인한 유저 아이디 저장 
              this.$store.dispatch('setToken')  // 토큰 state에 저장
            })
            .catch(err => {
              console.log(err)
            })
        })
        .catch(err => {
          console.log(err)
        })
    },  
    // 장르 선택 
    chooseGenres() {
      this.$axios({
        method: 'post',
        url: `${SERVER_URL}/movie/signup_like/`, 
        data: this.values,
      })
        .then(res => {
          this.movies = res.data
        })
        .catch(err => {
          console.log(err)
        })
    },
    // 회원가입 후 홈으로 가기
    signupDone() {
      this.$router.push({ name: 'Home'})
    },
    // 유효성 검사 
    validate() { // 회원가입
      if (this.$refs.form.validate()) {
        this.e1=2
        this.signup()
      }
    },
    validateGenre() { // 장르 
      if (this.$refs.genres.validate()) {
        this.e1=3
        this.chooseGenres()
      }
    },
    validateLike() { // 좋아요
      if (this.likeCount >= 2) {
        swal("환영합니다!", "회원가입이 완료되었습니다!", "success").then(
          this.$router.push({ name: 'Home' })
        )
      } else {
        swal("앗!", "영화를 두개 이상 선택해주세요!", "warning")
      }
    },
    // 영화 좋아요 개수
    likeCountMinus() {
      this.likeCount -= 1
    },
    likeCountPlus() {
      this.likeCount += 1
    }
  },

}
</script>

<style scoped>
.paddingForm {
  padding: 50px;
}
</style>
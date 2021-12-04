<template>
  <div>
    <v-container class="p-5">
      <h1 class="text-center">회원정보 수정</h1>
      <div class="d-flex align-items-center">
        <div class="me-3">닉네임: </div>
        <v-text-field v-model="nickname"
          regular
          placeholder="NICKNAME"
        ></v-text-field>
      </div>
      <!-- 이메일 -->
      <div class="d-flex align-items-center">
        <div class="me-3">이메일: </div>
        <v-text-field v-model="email"
          regular
          placeholder="EMAIL"
        ></v-text-field>
      </div>
      <!-- 파일업로드 -->
      <v-file-input v-model="files" name="files" label="upload profile image" @change="changeProfileImg"></v-file-input>
      <!-- 프로필 변경 -->
      <div class="d-flex align-items-center justify-center">
        <div class="d-flex flex-column align-items-center justify-center">
          <img :src="profileImage" alt="기존 프로필이미지" class="profile-img my-5">
          <h4>현재 프로필이미지</h4>
        </div>
        <v-icon x-large color="warning" class="mx-10">mdi-arrow-right-thick</v-icon>
        <div class="d-flex flex-column align-items-center justify-center">
          <img :src="newProfileImage" alt="새 프로필이미지" class="profile-img my-5">
          <h4>새 프로필이미지</h4>
        </div>
        <div class="ms-16">
          <!-- 비밀번호 변경 -->
          <div justify="center" class="my-5">
            <v-dialog
              v-model="dialog"
              persistent
              max-width="600px"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-btn outlined
                  large
                  v-bind="attrs"
                  v-on="on"
                >
                  비밀번호 변경
                </v-btn>
              </template>
              <v-card>
                <v-card-title>
                  비밀번호 변경
                </v-card-title>
                <v-card-text>
                  <v-container>
                    <v-row>
                      <v-col cols="12">
                        <v-text-field
                          label="Password*"
                          type="password"
                          required
                          v-model="password"
                          :rules="[rules.min, rules.required]"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12">
                        <v-text-field
                          label="New Password*"
                          type="password"
                          required
                          :rules="[rules.min, rules.required]"
                          v-model="newPassword"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12">
                        <v-text-field
                          label="New Password Confirmation*"
                          type="password"
                          required
                          :rules="[rules.match]"
                          v-model="newPasswordConfirmation"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                  </v-container>
                  <small>*indicates required field</small>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="blue darken-1"
                    text
                    @click="[dialog = false, setBack()]"
                  >
                    Close
                  </v-btn>
                  <v-btn
                    color="blue darken-1"
                    text
                    @click="[dialog = false, changePassword()]"
                  >
                    Submit
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </div>
          <!-- 업뎃 완료 버튼 -->
          <v-btn elevation="1" large
            color="primary" @click="changeUserInfo"
            class="mx-auto"
          >UPDATE</v-btn>
        </div>
      </div>
    <!-- 회원탈퇴 -->
    <v-btn
      elevation="2"
      plain
      rounded
      small
      @click="goToDelete"
      style="float:left"
    >회원 탈퇴</v-btn>
 </v-container>

</div>
</template>

<script>
// import ChangePassword from '@/views/accounts/ChangePassword'
import swal from 'sweetalert'

import { mapState } from 'vuex'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'ChangeProfile',
  components: {
    // ChangePassword
  },
  data() {
    return {
      nickname: null,
      email: null,
      profileImage: null,
      newProfileImage: 'https://mblogthumb-phinf.pstatic.net/MjAxODA0MTBfMjI2/MDAxNTIzMzY2MjI5Nzk0.xDtjpIX7dGFtPIY5sakKXpIF6295RrBbaF88VDSGyEEg.WRuXJKeZJNbiaNzyceStJLk7Imcn5fk3MpWZbn5g1wcg.JPEG.0ooz05/%EB%B9%84%EA%B3%B5%EA%B0%9C_%EC%95%84%EB%B0%94%ED%83%80.jpg?type=w800',
      files: null,
      dialog: false,
      password: '',
      newPassword: '',
      newPasswordConfirmation: '',
      rules: {
        required: value => !!value || `필수 입력 요소입니다.`,
        min: v => v.length >= 8 || '비밀번호는 8글자 이상입니다.',
        match: passwordCom => this.newPassword === passwordCom || '비밀번호가 일치하지 않습니다.',
      },
    }
  },
  methods: {
      setBack(){
        this.password = ''
        this.newPassword = ''
        this.newPasswordConfirmation = ''
      },
    // 유저 인증
      isUser() {
          const credentials = {
          username: this.userName,
          password: this.password
        }
        this.$axios({
          method: 'post',
          url: `${SERVER_URL}/accounts/api-token-auth/`,
          data: credentials,
          headers: this.config
        })
          .then(() => {
            this.password = null
            this.changePassword()
          })
          .catch(err => {
            console.log(err)
            swal ("비밀번호가 일치하지 않습니다.", {
            dangerMode: true,
          })
        })
      },
    // 비밀번호 변경 
      changePassword: function () {
          const credential2 = {
          password: this.newPassword,
          passwordConfirmation: this.newPasswordConfirmation
        }
        this.$axios({
          method: 'put',
          url: `${SERVER_URL}/accounts/change_password/`,
          data: credential2,
          headers: this.config
        })
          .then(() => {
            localStorage.removeItem('jwt')  // 기존 토큰 삭제 
            const credential3 = {
              username: this.userName,
              password: this.newPassword,
            }
            this.$axios({ // 새 토큰 발급 
              method: 'post',
              url: `${SERVER_URL}/accounts/api-token-auth/`,
              data: credential3,
              headers: this.config
            })
              .then(res => {
                localStorage.setItem('jwt', res.data.token)
                this.$emit('login')
                this.$store.dispatch('setToken')  // 토큰 state에 저장 
                swal ("비밀번호가 변경되었습니다.")
                this.$router.go() // 새로고침 
              })
              .catch(err => {
                console.log(err)
              })
          })
          .catch(err => {
            console.log(err)
          })
      },
    // 프로필 받아오기 
      getProfile() {
        this.$axios({
        method: 'get',
        url: `${SERVER_URL}/accounts/${this.userName}/`, 
        })
          .then(res => {
            this.nickname = res.data.nickname
            this.email = res.data.email
            if (res.data.profile_image === null) {
              this.profileImage = this.profileImg
            } else {
              this.profileImage = `http://127.0.0.1:8000${res.data.profile_image}`
              this.$store.dispatch('setUserProfileImg', res.data.profile_image)
            }
          })
          .catch(err => {
            console.log(err)
          })
      },
    // 회원 정보 수정 완료 
      changeUserInfo() {
        if (this.nickname === '') {
            swal ("닉네임을 입력해주세요.", {
            dangerMode: true,
          })
        }
        // 수정 데이터 넣기 
        let info = new FormData
        info.append('files', this.files);
        info.append('nickname', this.nickname);
        info.append('email', this.email);
        // 서버에 수정 요청 
        this.$axios({
          method: 'put',
          url: `${SERVER_URL}/accounts/change_profile/`,
          data: info,
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `JWT ${this.token}`
          }
        })
          .then(() => {
            this.getProfile()
            this.profileImage = 'https://mblogthumb-phinf.pstatic.net/MjAxODA0MTBfMjI2/MDAxNTIzMzY2MjI5Nzk0.xDtjpIX7dGFtPIY5sakKXpIF6295RrBbaF88VDSGyEEg.WRuXJKeZJNbiaNzyceStJLk7Imcn5fk3MpWZbn5g1wcg.JPEG.0ooz05/%EB%B9%84%EA%B3%B5%EA%B0%9C_%EC%95%84%EB%B0%94%ED%83%80.jpg?type=w800'
          })
          .catch(err => {
            console.log(err)
          })
      },
   // 프로필 이미지 미리보기 
      changeProfileImg(file) {
        this.newProfileImage = URL.createObjectURL(file)
        },
  // 회원 탈퇴로 이동
      goToDelete() {
        this.$router.push({ name: 'DeleteUser' })
      },
      },
      computed: {
        ...mapState(['userName', 'token', 'profileImg', 'config'])
      },
      created() {
        this.getProfile()
      }
  }
</script>

<style scoped>
.profile-img {
  border-radius: 100%;
  border-style: solid;
  border-width: 2px;
  height: 100px;
  width: 100px;
}
</style>
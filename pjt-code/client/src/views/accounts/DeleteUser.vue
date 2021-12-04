<template>
  <div>
    <v-container class="mt-16 d-flex flex-column align-items-center justify-center"  v-if="!confirm">
      <h1 class="mt-16">회원 탈퇴</h1>

      <v-text-field
        placeholder="비밀번호를 입력해주세요."
        type="password"
        required
        v-model="password"
        :rules="[rules.min, rules.required]"
        @keyup.enter="isUser"
      ></v-text-field>

      <v-btn
        elevation="1"
        large
        outlined
        rounded
        @click="isUser"
      >확인</v-btn>
    </v-container>
    <v-container v-else>
      <v-container fluid>
        <v-row align="center">
            <v-select
              :items="items"
              label="탈퇴 사유"
              solo
              v-model="reason"
            ></v-select>
        </v-row>
      </v-container>
      <v-textarea
        auto-grow
        solo
        v-model="detailReason"
        placeholder="탈퇴 사유를 구체적으로 입력해주세요."
      ></v-textarea>
      <v-btn
        elevation="1"
        large
        outlined
        rounded
        @click="check"
        style="float:right"
      >회원탈퇴</v-btn>
      
    </v-container>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import swal from 'sweetalert'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'DeleteUser',
  data() {
    return {
      confirm: false,
      password: '',
      items: ['서비스 불만', '개인정보 유출 우려', '사이트 이용 빈도 낮음', '지구 온난화 방지를 위한 PC사용 자제', '재 가입을 위해서', '기타'],
      detailReason: null,
      reason: null,
      rules: {
        required: value => !!value || `필수 입력 요소입니다.`,
        min: v => v.length >= 8 || '비밀번호는 8글자 이상입니다.',
        match: passwordCom => this.newPassword === passwordCom || '비밀번호가 일치하지 않습니다.',
      },
    }
  },
  methods: {
    // 유저 인증
    check() {
      swal({
          title: "정말로 삭제하시겠습니까?",
          text: "계정과 관련된 모든 정보가 삭제되며 복구할 수 없습니다.",
          icon: "warning",
          buttons: true,
          dangerMode: true,
        })
        .then((willDelete) => {
          if (willDelete) {
            this.deleteUser()
            swal("저희 사이트를 이용해 주셔서 감사합니다.", {
              icon: "success",
            })
          } else {
            swal("회원탈퇴가 취소되었습니다.")
            this.$router.push({ name: 'Home'})

          }
        });  
    },
    isUser() {
      if (this.password === '') {
          swal ("비밀번호를 입력하세요.", {
          dangerMode: true,
        })
      }
      const credentials = {
        username: this.userName,
        password: this.password
      }
      this.$axios({
        method: 'post',
        url: `${SERVER_URL}/accounts/api-token-auth/`,
        data: credentials,
      })
        .then(() => {
          this.confirm = true
        })
        .catch(err => {
          console.log(err)
        })
    },
    // 회원탈퇴
    deleteUser: function () {
      const deleteInfo = {
        reason: this.reason,
        detailReason: this.detailReason
      }
      this.$axios({
        method: 'delete',
        url: `${SERVER_URL}/accounts/withdrawal/`, 
        data: deleteInfo,
        headers: this.config
      })
        .then(() => {
          localStorage.removeItem('jwt')  // 기존 토큰 삭제 
          this.$router.push({ name: 'Home' })
          this.$store.dispatch('deleteUserName')
        })
        .catch(err => {
          console.log(err)
        })
    }
  },
  computed: {
    ...mapState(['userName', 'config'])
  }
}
</script>

<style scoped>

</style>
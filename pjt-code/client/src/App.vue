<template>
  <v-app>
    <v-app-bar color="white" absolute shrink-on-scroll scroll-target="#scrolling-techniques-2" fade-img-on-scroll prominent
      elevation="1"
      class="mainFont">

      <template v-slot:img="{ props }">
        <img :src="require(`@/assets/8de6ea134a2719f9.png`)" v-bind="props" style="padding-left:375px;" class="py-3">
      </template>
      <v-row>
        <!-- home -->
        <v-col cols="8">
          <router-link :to="{ name: 'Home' }" 
            class="text-decoration-none black--text mx-3" 
          >HOME</router-link>
          <!-- 자유게시판 -->
          <router-link :to="{ name: 'Board' }" 
              class="text-decoration-none black--text mx-3"
            >BOARD</router-link>
            <!-- 영화 추천 -->
            <router-link :to="{ name: 'MovieRecommend' }"
              class="text-decoration-none black--text mx-3"
            >RECOMMEND</router-link>
          <!-- </div> -->
        </v-col>
        <!-- 검색창 -->
        <v-col cols="3" >
          <v-text-field v-model.trim="searchMovie" @keyup.enter="goToSearchPage" 
            placeholder="검색어를 입력하세요" dense label="Search Movie" class="searchBar">
          <v-icon slot="append" @click="goToSearchPage">mdi-magnify</v-icon>
          </v-text-field>
        </v-col>

        <v-col cols="1" class="pt-0">
          <!-- 프로필 이미지 -->
          <v-menu bottom min-width="150px" rounded offset-y>
            <template v-slot:activator="{ on }">
              <v-btn icon x-large v-on="on">
                <v-avatar color="white" size="48">
                  <!-- <span class="black--text text-h5">JS</span> -->
                  <!-- 로그인 -->
                  <img :src="profileImg" alt="" height="70" v-if="userName">
                  <!-- 비로그인 -->
                  <img :src="baseProfileImg" alt="" height="70" v-else>
                </v-avatar>
              </v-btn>
            </template>
          <!-- 프로필 이미지 눌렀을때 메뉴 -->
            <v-card>
              <v-list-item-content class="justify-center">
                <!-- 로그인 -->
                <div class="mx-auto text-center" v-if="userName">
                  <!-- 프로필 -->
                  <router-link :to="{ name: 'Profile', params: { userName: this.userName } }"
                    class="text-decoration-none black--text"
                  ><v-btn depressed rounded text>MY PROFILE</v-btn></router-link>
                  <v-divider class="my-3"></v-divider>
                  <!-- 프로필 수정 -->
                  <router-link :to="{ name: 'ChangeProfile' }"
                    class="text-decoration-none black--text"
                  ><v-btn depressed rounded text>SETTING</v-btn></router-link>
                  <v-divider class="my-3"></v-divider>
                  <!-- 로그아웃 -->
                  <router-link to="#" @click.native="logout"
                    class="text-decoration-none black--text"
                  ><v-btn depressed rounded text>LOGOUT</v-btn></router-link>
                  <!-- 관리자 페이지 -->
                  <div v-if="isAdmin">
                    <v-divider class="my-3"></v-divider>
                    <a href="http://127.0.0.1:8000/admin/" class="text-decoration-none black--text">
                      <v-btn depressed rounded text>ADMIN</v-btn>
                    </a>
                  </div>
                </div>
                <!-- 비로그인 -->
                <div class="mx-auto text-center" v-else>
                  <!-- 회원가입 -->
                  <router-link :to="{ name: 'Signup' }"
                    class="text-decoration-none black--text"
                  ><v-btn depressed rounded text>SIGNUP</v-btn></router-link>
                  <v-divider class="my-3"></v-divider>
                  <!-- 로그인 -->
                  <router-link :to="{ name: 'Login' }"
                    class="text-decoration-none black--text"
                  ><v-btn depressed rounded text>LOGIN</v-btn></router-link>
                </div>
              </v-list-item-content>
            </v-card>
          </v-menu>
        </v-col>
      </v-row>
    </v-app-bar>

    <!-- 본문 -->
    <v-sheet
      id="scrolling-techniques-2"
      class="overflow-y-auto padding"
      max-height="100vh"
    >
      <v-main style="height: 1000px;" class="mainFont">
        <router-view :key="$route.fullPath"/>
      </v-main> 
    </v-sheet>
  </v-app>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'App',
  data: function () {
    return {
      searchMovie: '', // 영화 키워드 
      baseProfileImg: 'https://mblogthumb-phinf.pstatic.net/MjAxODA0MTBfMjI2/MDAxNTIzMzY2MjI5Nzk0.xDtjpIX7dGFtPIY5sakKXpIF6295RrBbaF88VDSGyEEg.WRuXJKeZJNbiaNzyceStJLk7Imcn5fk3MpWZbn5g1wcg.JPEG.0ooz05/%EB%B9%84%EA%B3%B5%EA%B0%9C_%EC%95%84%EB%B0%94%ED%83%80.jpg?type=w800',
   }
  },
  methods: {
    // 로그아웃 
    logout() {
      localStorage.removeItem('jwt')
      this.$store.dispatch('deleteUserName')
      this.$router.push({ name: 'Login' })
    },
    // 검색창 이동
    goToSearchPage() {
      this.$router.push({ name: 'SearchMovie', params: { keyword: this.searchMovie } }).catch(()=> {})
    },
  },
  computed: {
    ...mapState(['userName', 'profileImg', 'isAdmin'])
  },
  watch: {
    userProfileImg() {
      this.userProfileImg = this.profileImg
    },
  }
}
</script>


<style lang="scss">
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@700&family=Playfair+Display+SC:wght@900&display=swap?family=Noto+Sans+KR:wght@500&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@500&display=swap');
.notosans {
  font-family: 'Noto Sans KR', sans-serif;
}
.application {
  font-family: 'Playfair Display SC', serif;  
}
.mainFont {
  font-family: 'JetBrains Mono','Noto Sans KR', monospace;
}
.padding{
  padding-top:150px
}
:v-deep .v-text-field__details {
  display: none;
}
.v-app-bar {
  z-index: 100 !important;
}
</style>
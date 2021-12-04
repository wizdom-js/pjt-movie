<template>
  <div>
    <v-row class="d-flex d-column align-items-end">
      <v-col md="2"><h1 class="mb-5">BOARD</h1></v-col>
      <v-col md="4" offset-md="6" class="searchInput mb-1">
        <v-text-field v-model.trim="searchKeyword" @keyup.enter="searchPost" 
            placeholder="검색어를 입력하세요" dense flat shaped label="SEARCH POST" color="orange">
          <v-icon slot="append" @click="searchPost">mdi-magnify</v-icon>
        </v-text-field>
      </v-col>
    </v-row>
    <v-simple-table :current-page="currentPage">
      <thead>
        <tr>
          <th class="text-center">ORDER</th>
          <th class="text-center">TITLE</th>
          <th class="text-center">USER</th>
          <th class="text-center">DATE</th>
        </tr>
      </thead>
      <!-- 게시글 목록 -->
      <tbody v-if="isPost">
        <tr v-for="(post, index) in posts"
          :key="post.id"
          @click="postDetail(post.id)">
          <td class="text-center">{{ index + 1 }}</td>
          <td class="text-center" >{{ post.title }}</td>
          <td class="text-center">
            <img :src="getUserProfileImg(post.profile_img)" class="profileImg" >
            {{ post.nickname }}
          </td>
          <td class="text-center" >{{ post.created_at }}</td>
        </tr>
      </tbody>
      <!-- 게시글 없을때 -->
      <tbody v-else>
        <td colspan="12" rowspan="3" class="text-center py-5">"{{ searchBeforeKeyword }}" 에 해당하는 게시글이 없습니다.</td>
      </tbody>
    </v-simple-table>

    <!-- 하단 버튼 -->
    <v-row class="my-5">
    <!-- pagination -->
      <v-col offset-md="4" md="4">
        <v-pagination
          v-model="currentPage"
          :length="totalPage"
          @input="goToPage"
          :max-pages="3"
        ></v-pagination>
      </v-col>
      <v-col offset-md="2" md="1">
        <b-button @click="postCreate" squared variant="outline-dark" class="py-2 px-5">Create</b-button>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import _ from 'lodash'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'PostList',
  data() {
    return {
      posts: null,
      searchKeyword: null,
      searchBeforeKeyword: null,
      isPost: true,
      currentPage: 1,
      totalPage: 1, 
    }
  },
  methods: {
    // 클릭한 게시글로 이동 
    postDetail(id) {
      this.$router.push({ name: 'PostDetail', params: { postNum: id } })
    },
    // 전체 게시글 서버에서 불러오기 
    getPosts() {
      this.$axios({
        method: 'get',
        url: `${SERVER_URL}/community/`,
        params: {page: this.currentPage}
      })
        .then(res => {
          const temp = _.slice(res.data, 0, res.data.length-1)
          this.totalPage = _.last(res.data).possible_page
          this.posts = temp.map(post => {
            const newInfo = {
              title: post.title,
              id: post.id,
              created_at: _.join(_.slice(post.created_at, 0, 10), ''),
              username: post.user.username,
              profile_img: post.user.profile_image,
              nickname: post.user.nickname,
            }
            return newInfo
          })
        })
        .catch(err => {
          console.log(err)
        })
    },
    // 날짜 슬라이싱 
    changeDate(date) {
      return _.join(_.slice(date, 0, 10), '')
    },
    // 페이지 이동
    goToPage() {
      this.getPosts()
    },
    // 게시글 검색
    searchPost() {
      this.$axios({
        method: 'get',
        url: `${SERVER_URL}/community/${this.searchKeyword}/search/`,
      })
        .then(res => {
          const temp = res.data
          this.isPost = this.posts.length > 0 ? true : false
          this.searchBeforeKeyword = this.searchKeyword
          this.searchKeyword = null
          this.posts = temp.map(post => {
            const newInfo = {
              title: post.title,
              id: post.id,
              created_at: _.join(_.slice(post.created_at, 0, 10), ''),
              username: post.user.username,
              profile_img: post.user.profile_image,
              nickname: post.user.nickname,
            }
            return newInfo
          })
        })
        .catch(err => {
          console.log(err)
        })
    },
    // 프로필 이미지
    getUserProfileImg(img) { 
      if (img === null) {
        return 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQU00i-_pNcxxQ69OH2c8MyVuHS0Q4GdMDR7w&usqp=CAU'
      } else {
        return `http://127.0.0.1:8000${img}`
      }
    },
    // 게시글 작성 
    postCreate() {
      const token = localStorage.getItem('jwt')
      if (token) { // 로그인 상태 -> 게시글 생성 
        this.$router.push({ name: 'PostCreate', params: { postId: 0 }})
      } else {    // 비로그인 상태 -> 로그인 
        this.$router.push({ name: 'Login' })
      }
    },
  },
  created() {
    this.getPosts()
  }
}
</script>

<style scoped lang="scss">
.searchInput {
  margin-bottom: -30px;
}
.profileImg {
  height: 30px;
  width: 30px;
  border-style: solid;
  border-width: 1px;
  border-radius: 100%;
}
</style>

<style scoped>
::v-deep .v-pagination__item {
  border-radius: 0px;
  margin: 0px;
  box-shadow: none;
}
::v-deep .v-pagination__item--active.primary {
  background-color: black !important;
}
::v-deep .v-pagination__navigation {
  border-radius: 0px;
}
::v-deep th {
  background-color: black;
  color: white !important;
  font-size: 15px !important;
}
</style>
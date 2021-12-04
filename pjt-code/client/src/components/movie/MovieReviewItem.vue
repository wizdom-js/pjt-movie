<template>
  <div>
    <!-- 조회 -->
    <div v-if="!isUpdate">
      <v-row v-if="oldReview">
        <v-col cols="7" style="position:relative;">
          <div class="d-flex align-items-center">
            <v-rating background-color="grey" color="warning" hover readonly v-model="rank" 
              ></v-rating>
            <div>{{ rank }}</div>
          </div>
          <!-- 스포 -->
          <div v-if="isSpoiler" style="position:absolute;" class="px-3 my-3 spoiler d-flex">
            <p class="me-1">스포일러가 포함된 내용입니다.</p>
            <a href="#" @click="isSpoiler=false">감상평 보기</a>
          </div>
          <div class="px-3 my-3">{{ oldReview.content }}</div>
          <div class="px-3">{{ changeDate(oldReview.created_at) }}</div>
        </v-col>
        <v-col cols="3" class="d-flex flex-column justify-end" @click="goToProfile()">
          <img :src="getUserProfileImg()" alt="프로필이미지" class="profileImg">
          <div>{{ oldReview.user.nickname }}</div>
        </v-col>
        <v-col v-if="isSameUser" cols="2" class="d-flex flex-column align-items-end justify-end">
          <v-btn @click="showInput" outlined class="udBtn">update</v-btn>
          <v-btn @click="deleteReview" plain outlined class="udBtn">delete</v-btn>
        </v-col>
        <v-col v-else cols="2">

        </v-col>
        <v-divider></v-divider>
      </v-row>
      <div v-else>
        아직 리뷰가 없습니다 ! 영화의 리뷰를 남겨보세요
      </div>
    </div>
    <!-- 수정 -->
    <div v-else>
      <div class="d-flex flex-column">
    <div class="d-flex align-items-center">
      <v-rating v-model="rank"
        color="warning" background-color="grey"
        hover large
      ></v-rating>
      <div class="mx-3 text-h5">{{ rank }}</div>
    </div>
    <v-checkbox :value="isSpoiler" v-model="isSpoiler" label="스포일러를 포함한 내용인가요?"></v-checkbox>
    <div class="d-flex align-items-end">
      <v-text-field v-model.trim="newReview" @keyup.enter="updateReview()"
        outlined label="감상평을 수정해주세요."
      ></v-text-field>
      <div class="d-flex flex-column mx-3">
        <v-btn @click="updateReview()" outlined>수정</v-btn>
        <v-btn @click="isUpdate = !isUpdate" outlined class="my-2">취소</v-btn>
      </div>
    </div>
      </div>
    </div>
  <!-- </div>
      <input type="number" v-model="rank" value="별점">
      <v-checkbox value="True" v-model="isSpoiler" label="스포일러를 포함한 내용인가요?"></v-checkbox>
      <v-text-field v-model.trim="newReview" color="error" @keyup.enter="updateReview"></v-text-field>
      <button @click="updateReview">+</button>
      <button @click="isUpdate = !isUpdate">취소</button>
    </div> -->
  </div>
</template>

<script>
import { mapState } from 'vuex'
import _ from 'lodash'
const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'MovieReviewItem',
  props: {
    oldReview: Object,
    reloadReview: Function
  },
  data() {
    return {
      newReview: null,
      rank: this.oldReview.rank,
      isSpoiler: this.oldReview.is_spoiler,
      isSameUser: null,
      isUpdate: false,
    }
  },
  methods: {
    // 리뷰작성자 프로필로 이동 
    goToProfile() {
      this.$router.push({ name: 'Profile', params: { userName: this.oldReview.user.username } })
    },
    // 리뷰 삭제 
    deleteReview() {
      this.$axios({
        method: 'delete',
        url: `${SERVER_URL}/movie/${this.$route.params.movieId}/review/${this.oldReview.id}/`, 
        headers: this.config
      })
        .then(() => {
          this.reloadReview()
        })
        .catch(err => {
          console.log(err)
        })
    },
    // 리뷰 업뎃 
    updateReview() { 
      const reviewItem = {
        content: this.newReview,
        rank: this.rank,
        is_spoiler: this.isSpoiler ? true : false,
      }
      this.$axios({
        method: 'put',
        url: `${SERVER_URL}/movie/${this.$route.params.movieId}/review/${this.oldReview.id}/`, 
        data: reviewItem,
        headers: this.config
      })
        .then(() => {
          this.reloadReview()
          this.isUpdate = !this.isUpdate
        })
        .catch(err => {
          console.log(err)
        })
    },
    // 수정 버튼 눌렸을 때, input창 나타내기 
    showInput() { 
      this.isUpdate = !this.isUpdate
      this.newReview = this.oldReview.content
      this.rank = this.oldReview.rank
      this.isSpoiler = this.oldReview.is_spoiler
    },
    // 프로필 이미지
    getUserProfileImg() {
      if (this.oldReview.user.profile_image === null) {
        return 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQU00i-_pNcxxQ69OH2c8MyVuHS0Q4GdMDR7w&usqp=CAU'
      } else {
        return `http://127.0.0.1:8000${this.oldReview.user.profile_image}`
      }
    },
    // 날짜 수정
    changeDate(date) {
      return _.join(_.slice(date, 0, 10), '')
    }
  },
  computed: {
    ...mapState(['config', 'userName'])
  },
  created() {
    if (this.userName === this.oldReview.user.username) {
         this.isSameUser = true
    }
  }
  // watch: {
  //   oldReview() {
  //     if (this.userName === this.oldReview.user.username) {
  //       this.isSameUser = true
  //     }
  //   }
  // }
}
</script>

<style scoped>
.hide {
  display: none;
}
.profileImg {
  height: 50px;
  width: 50px;
  border-style: solid;
  border-radius: 100%;
}
.udBtn {
  border-style: none;
  padding-left: 5px;
  padding-right: 5px;
}
::v-deep .v-text-field__details {
  display: none;
}
.spoiler {
  background-color: white;
}
</style>
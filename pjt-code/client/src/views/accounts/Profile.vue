<template>
  <v-container>
    <v-row>
      <v-col cols="4" class="d-flex flex-column align-items-center justify-content-center"> 
        <img :src="getUserProfileImg()" :alt="`${ userProfile.nickname }님의 프로필 사진`" class="profileImg">
        <h1>{{ userProfile.nickname }}</h1>
        <!-- 팔로우 / 언팔 버튼 -->
        <div v-if="this.userName != this.$route.params.userName" class="mt-8 mb-4">
          <v-btn v-if="followState" @click="changeFollowState" color="info" outlined>
            <v-icon left>mdi-account-check</v-icon>UNFOLLOW
          </v-btn>
          <v-btn v-else @click="changeFollowState" color="info"
            ><v-icon left>mdi-account-plus</v-icon>FOLLOW
          </v-btn>
        </div>
        <!-- 정보 조회 탭 -->
        <v-tabs vertical class="mt-4">
          <v-tab class="tab" @click="chooseContent('follow')"><v-icon left>mdi-account-group</v-icon>FOLLOW</v-tab>
          <v-tab class="tab" @click="chooseContent('like')"><v-icon left>mdi-heart-multiple</v-icon>LIKE</v-tab>
          <v-tab class="tab" @click="chooseContent('history')"><v-icon left>mdi-pen</v-icon>HISTORY</v-tab>
        </v-tabs>
      </v-col>

      <v-col cols="8">
      <v-card>
      <!-- 팔로우 팔로워 -->
        <div v-if="showFollow">
          <v-tabs fixed-tabs >
            <v-tab @click="chooseFollow(true)">
                <v-badge color="orange" :content="followingCount">FOLLOWING</v-badge>
            </v-tab>
            <v-tab @click="chooseFollow(false)">
              <v-badge color="orange" :content="followerCount">FOLLOWER</v-badge>
            </v-tab>
          </v-tabs>
          <v-card class="overflow-y-auto" height="600px" elevation="0">
            <div v-if="showFollowing">
              <following-list 
                :followings="userProfile.followings"
                :followingsCount="userProfile.followings_count"
                @unfollow="decreaseFollowingCount"
                @follow="increaseFollowingCount"
              ></following-list>
            </div>
            <div v-if="showFollower">
              <follower-list 
                :followers="userProfile.followers"
                :followersCount="userProfile.followers_count"
                @delete-follower="decreaseFollowerCount"
              ></follower-list>
            </div>
          </v-card>
        </div>

       <!-- 유저가 좋아요한 것들 -->
        <div v-if="showLike">
          <v-tabs fixed-tabs >
            <v-tab @click="chooseLike(true)">
                <v-badge color="orange" :content="likeMovieCount">MOVIE</v-badge>
            </v-tab>
            <v-tab @click="chooseLike(false)">
              <v-badge color="orange" :content="likePostCount">POST</v-badge>
            </v-tab>
          </v-tabs> 
          <v-card class="overflow-y-auto" height="600px" elevation="0">
            <div v-if="showLikeM">
              <like-movie-list 
                :like-movies="userProfile.like_movie"></like-movie-list>
            </div>
            <div v-if="showLikeP">
              <like-post-list 
                :like-posts="userProfile.like_posts"
                :like-post-count="userProfile.like_post_count"
              ></like-post-list> 
            </div>
          </v-card>
        </div>
        
        <!-- 유저가 작성한 글 -->
        <div v-if="showMy">
          <v-tabs fixed-tabs >
            <v-tab @click="chooseHistory('review')">
                <v-badge color="orange" :content="myReviewCount">REVIEW</v-badge>
            </v-tab>
            <v-tab @click="chooseHistory('post')">
              <v-badge color="orange" :content="myPostCount">POST</v-badge>
            </v-tab>
            <v-tab @click="chooseHistory('comment')">
              <v-badge color="orange" :content="myCommentCount">COMMENT</v-badge>
            </v-tab>
          </v-tabs>
          <v-card class="overflow-y-auto" height="600px" elevation="0">
            <div v-if="showMyR">
              <my-review-list 
                :review-set="userProfile.review_set"
                :review-count="userProfile.review_count"
              ></my-review-list>
            </div>
            <div v-if="showMyP">
              <my-post-list 
                :post-set="userProfile.post_set"
                :post-count="userProfile.post_count"
              ></my-post-list>
            </div>
            <div v-if="showMyC">
              <my-comment-list 
                :comment-set="userProfile.comment_set"
                :comment-count="userProfile.comment_count"
              ></my-comment-list>
            </div>
          </v-card>
        </div>
      </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import FollowingList from '@/components/accounts/follow/FollowingList'
import FollowerList from '@/components/accounts/follow/FollowerList'
import MyReviewList from '@/components/accounts/my/MyReviewList'
import MyPostList from '@/components/accounts/my/MyPostList'
import MyCommentList from '@/components/accounts/my/MyCommentList'
import LikeMovieList from '@/components/accounts/like/LikeMovieList'
import LikePostList from '@/components/accounts/like/LikePostList'
import { mapState } from 'vuex'
import _ from 'lodash'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'Profile',
  components: {
    FollowingList,
    FollowerList,
    MyReviewList,
    MyPostList,
    MyCommentList,
    LikeMovieList,
    LikePostList
  },
  data() {
    return {
      userProfile: '',
      userProfileImg: '',
      followState: true,
      followerCount: 0,
      followingCount: 0,
      likeMovieCount: 0,
      likePostCount: 0,
      myReviewCount: 0,
      myPostCount: 0,
      myCommentCount: 0,
      
      // 숨기기 값들 
      showFollow: true,
      showMy: false,
      showLike: false,
      showFollowing: true,
      showFollower: false,
      showMyR: true,
      showMyP: false,
      showMyC: false,
      showLikeM: true,
      showLikeP: false,
    }
  },
  methods: {
    // ------ 버튼 클릭 --------
    // 큰 탭 선택 
    chooseContent(tab) {
      if (tab === 'follow') {
        this.showFollow = true
        this.showLike = false
        this.showMy = false
      } else if (tab === 'like') {
        this.showFollow = false
        this.showLike = true
        this.showMy = false
      } else {
        this.showFollow = false
        this.showLike = false
        this.showMy = true
      }
    },
    // 팔로우 선택 
    chooseFollow(tab) {
      if (tab) {
        this.showFollowing = true
        this.showFollower = false
      } else {
        this.showFollowing = false
        this.showFollower = true
      }
    },
    // 좋아요 선택 
    chooseLike(tab) {
      if (tab) {
        this.showLikeM = true
        this.showLikeP = false
      } else {
        this.showLikeM = false
        this.showLikeP = true
      }
    },
    // 기록 선택 
    chooseHistory(tab) {
      if (tab === 'review') {
        this.showMyR = true
        this.showMyP = false
        this.showMyC = false
      } else if (tab === 'post') {
        this.showMyR = false
        this.showMyP = true
        this.showMyC = false
      } else {
        this.showMyR = false
        this.showMyP = false
        this.showMyC = true
      }
    },
    // 프로필 받아오기 
    getProfile() {
      this.$axios({
        method: 'get',
        url: `${SERVER_URL}/accounts/${this.$route.params.userName}/`, 
      })
        .then(res => {
          this.userProfile = res.data
          this.followerCount = res.data.followers_count
          this.followingCount = res.data.followings_count
          this.likeMovieCount = res.data.like_movie.length
          this.likePostCount = res.data.like_post_count
          this.myReviewCount = res.data.review_count
          this.myPostCount = res.data.post_count
          this.myCommentCount = res.data.comment_count
        })
        .then(() => {
          this.didFollow()
        })
        .catch(err => {
          console.log(err)
        })
    },
    // 프로필 이미지
    getUserProfileImg() {
      if (this.userProfile.profile_image === null) {
        return 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQU00i-_pNcxxQ69OH2c8MyVuHS0Q4GdMDR7w&usqp=CAU'
      } else {
        return `http://127.0.0.1:8000${this.userProfile.profile_image}`
      }
    },
    // follower 수 감소
    decreaseFollowerCount() {
      this.followerCount -= 1
    },
    // following 수 감소
    decreaseFollowingCount() {
      this.followingCount -= 1
    }, 
    // following 수 증가
    increaseFollowingCount() {
      this.followingCount += 1
    },

    // follow 했는지 알아보기
    didFollow() {
      this.followState = _.some(this.userProfile.followers, ['username', this.userName])
    },
    // follow 또는 언팔 하기 
    changeFollowState() {
      if (this.config) {
        this.$axios({
        method: 'post',
        url: `${SERVER_URL}/accounts/${this.$route.params.userName}/follow/`,
        headers: this.config
      })
        .then(() => {
          this.getProfile()
        })
        .catch(err => {
          console.log(err)
        })
      } else {
        this.$router.push({ name: 'Login' })
      }
    }
  },
  created() {
    this.getProfile()
  },
  computed: {
    ...mapState(['userName', 'config', 'profileImg'])
  }
}
</script>

<style scoped>
.hide {
  display: none;
}
.tab {
  height:50px;
}
.v-card {
  max-height: 100%;
}
.profileImg {
  height: 300px;
  width: 300px;
  border-radius: 100%;
}
</style>
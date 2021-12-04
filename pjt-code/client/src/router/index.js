import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from '@/views/Home'
const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
    return originalPush.call(this, location).catch(() => {
        return window.location.reload()
    })
};

// 자유게시판
import Board from '@/views/board/Board'
import PostDetail from '@/views/board/PostDetail'
import PostCreate from '@/views/board/PostCreate'

// 유저
import Profile from '@/views/accounts/Profile'
import Signup from '@/views/accounts/Signup'
import Login from '@/views/accounts/Login'
import ChangeProfile from '@/views/accounts/ChangeProfile'
import DeleteUser from '@/views/accounts/DeleteUser'

// 영화 
import MovieDetail from '@/views/movie/MovieDetail'
import MovieRecommend from '@/views/movie/MovieRecommend'
import IsAdult from '@/views/movie/IsAdult'
import SearchMovie from '@/views/movie/SearchMovie'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  
  // 자유게시판 
  {
    path: '/board',
    name: 'Board',
    component: Board
  },
  {
    path: '/board/:postNum',
    name: 'PostDetail',
    component: PostDetail
  },
  {
    path: '/board/create/:postId',
    name: 'PostCreate',
    component: PostCreate
  },

  // 유저
  {
    path: '/signup',
    name: 'Signup',
    component: Signup
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/profile/:userName',
    name: 'Profile',
    component: Profile
  },
  // 회원 정보 수정 
  {
    path: '/change-userinfo',
    name: 'ChangeProfile',
    component: ChangeProfile
  },
  // 회원 탈퇴
  {
    path: '/delete-userinfo',
    name: 'DeleteUser',
    component: DeleteUser
  },

  // 성인 영화
  {
    path: '/movie/forbidden',
    name: 'IsAdult',
    component: IsAdult
  },
  // 영화 조회 
  {
    path: '/movie/:movieId',
    name: 'MovieDetail',
    component: MovieDetail
  },
  // 상세 추천
  {
    path: '/recommend',
    name: 'MovieRecommend',
    component: MovieRecommend
  },
  // 영화 검색
  {
    path: '/search/:keyword',
    name: 'SearchMovie',
    component: SearchMovie
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

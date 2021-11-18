import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)
const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default new Vuex.Store({
  plugins: [createPersistedState()],
  state: {
    posts: [],
    post: null,
    userName: null,
    token: null,
    config: null,
  },
  mutations: {
    SET_USERNAME(state, userName) {
      state.userName = userName
    },
    DELETE_USERNAME(state) {
      state.userName = null
    },
    GET_POSTS(state, posts) {
      state.posts = posts
    },
    SET_TOKEN(state, token) {
      state.token = token
      state.config = {
        Authorization: `JWT ${token}` 
      }
    }
  },
  actions: {
    // 유저 네임 저장 
    setUserName({ commit }, userName) {
      commit('SET_USERNAME', userName)
    },
    // 유저 삭제
    deleteUserName({ commit }) {
      commit('DELETE_USERNAME')
    },
    setToken({ commit }) {
      commit('SET_TOKEN', localStorage.getItem('jwt'))
    },
    // 자유게시판 전체 글 가져오기 
    getPosts({ commit }) {
      axios({
        method: 'get',
        url: `${SERVER_URL}/community/`,
        // headers: this.state.userInfo.config
      })
        .then(res => {
          commit('GET_POSTS', res.data)
        })
        .catch(err => {
          console.log(err)
        })
    },
  },
  modules: {
  }
})

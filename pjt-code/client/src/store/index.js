import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

export default new Vuex.Store({
  plugins: [createPersistedState()],
  state: {
    userName: null,
    profileImg: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQU00i-_pNcxxQ69OH2c8MyVuHS0Q4GdMDR7w&usqp=CAU',
    token: null,
    config: null,
    isAdmin: null,
  },
  mutations: {
    SET_USERNAME(state, userName) {
      state.userName = userName
    },
    DELETE_USERNAME(state) {
      state.userName = null
      state.profileImg = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQU00i-_pNcxxQ69OH2c8MyVuHS0Q4GdMDR7w&usqp=CAU'
      state.token = null
      state.config = null
      state.isAdmin = null
    },
    SET_TOKEN(state, token) {
      state.token = token
      state.config = {
        Authorization: `JWT ${token}` 
      }
    },
    SET_USER_PROFILE_IMG(state, profileImg) {
      if (profileImg != null) {
        state.profileImg = `http://127.0.0.1:8000${profileImg}`
      }
    },
    SET_IS_ADMIN(state, isAdmin) {
      state.isAdmin = isAdmin
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
    // 프로필 이미지 저장
    setUserProfileImg({ commit }, profileImg) {
      commit('SET_USER_PROFILE_IMG', profileImg)
    },
    // 관리자 여부 저장
    setIsAdmin({ commit }, isAdmin) {
      commit('SET_IS_ADMIN', isAdmin)
    }
  },
  modules: {
  }
})

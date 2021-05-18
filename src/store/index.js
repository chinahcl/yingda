import Vue from 'vue'
import Vuex from 'vuex'
import user from './user'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    Authorization: localStorage.getItem('Authorization') ? localStorage.getItem('Authorization') : ''
  },
  mutations: {
    changeLogin (state, user) {
      state.Authorization = user.Authorization
      localStorage.setItem('Authorization', user.Authorization)
    }
  },
  actions: {
  },
  modules: {
    user
  }
})

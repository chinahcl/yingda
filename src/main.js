import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'

Vue.prototype.axios = axios
Vue.config.productionTip = false
Vue.use(ElementUI)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

// 异步请求前在header里加入token
axios.interceptors.request.use(
  config => {
    if (config.url === '/logins') { // 如果是登录和注册操作，则不需要携带header里面的token
    } else {
      if (localStorage.getItem('Authorization')) {
        config.headers.Authorizatior = localStorage.getItem('Authorization')
      }
    }
    // console.log(config)
    return config
  },
  error => {
    return Promise.reject(error)
  })
// 异步请求后，判断token是否过期
axios.interceptors.response.use(
  response => {
    return response
  },
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          localStorage.removeItem('Authorization')
          this.$router.push('/')
      }
    }
  }
)
// 异步请求前判断请求的连接是否需要token
router.beforeEach((to, from, next) => {
  // console.log('异步请求', to.path)
  if (to.path === '/') {
    next()
  } else {
    const token = localStorage.getItem('Authorization')
    console.log('我是浏览器本地缓存的token: ' + token)
    if (token === 'null' || token === '') {
      next('/')
    } else {
      next()
    }
  }
})

// // 全局拦截器,在进入需要用户权限的页面前校验是否已经登录
// router.beforeResolve((to, from, next) => {
//   const loginUser = store.state.user.user
//   // 判断路由是否设置相应校验用户权限
//   if (to.meta.requireAuth) {
//     console.log('拦截')
//     console.log(to.meta.requireAuth)
//     if (!loginUser) {
//       // 没有登录，显示登录组件
//       store.dispatch('setShowLogin', true)
//       if (from.name == null) {
//         // 此时，是在页面没有加载，直接在地址栏输入链接，进入需要登录验证的页面
//         next('/')
//         return
//       }
//       // 终止导航
//       next(false)
//       return
//     }
//   }
//   next()
// })

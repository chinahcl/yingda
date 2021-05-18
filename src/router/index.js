import Vue from 'vue'
import VueRouter from 'vue-router'
// import LoginRouter from './login'
// import RegisterRouter from './register'
import IndexRouter from './index_1'
// import test from '@/router/test'
import logins from '@/router/logins'
import Index2Router from './index_2'
import RoBotRouter from './robot'
import RoBotManageRouter from './robot_manage'

Vue.use(VueRouter)

const routes = [
  IndexRouter,
  Index2Router,
  RoBotRouter,
  RoBotManageRouter,
  logins,
  {
    path: '/*',
    redirect: '/logins'
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

// 导航守卫
// 使用 router.beforeEach 注册一个全局前置守卫，判断用户是否登陆
router.beforeEach((to, from, next) => {
  const token = localStorage.yun_user
  console.log(to.path)
  if (to.path === '/logins') {
    if (token === '' || token === undefined) {
      next()
      return
    } else {
      console.log('logins1111')
      if (to.path === '/logins' && token !== undefined) {
        next('/index_1')
        return
      }
      next(to.path)
    }
    next(to.path)
  } else {
    console.log(localStorage.yun_user)
    if (token === 'null' || token === undefined || token === '') {
      next('/logins')
    } else {
      next()
    }
  }
})

export default router

export default {
  path: '/robot_manage',
  component: () => import('@/views/Index_1'),
  name: 'robot_manage',
  children: [
    {
      path: 'run_state_robot',
      component: () => import('@/views/robot_manage/run_state_robot.vue'),
      name: 'run_state_robot'
    },
    {
      path: 'single_add_robot',
      component: () => import('@/views/robot_manage/single_add_robot.vue'),
      name: 'single_add_robot'
    },
    {
      path: 'fronzen_robot',
      component: () => import('@/views/robot_manage/fronzen_robot.vue'),
      name: 'fronzen_robot'
    },
    {
      path: 'thaw_robot',
      component: () => import('@/views/robot_manage/thaw_robot.vue'),
      name: 'thaw_robot'
    },
    {
      path: 'query_robot',
      component: () => import('@/views/robot_manage/query_robot.vue'),
      name: 'query_robot'
    },
    {
      path: 'change_robot',
      component: () => import('@/views/robot_manage/change_robot.vue'),
      name: 'change_robot'
    }
    // {
    //   path: '/robot_manage',
    //   redirect: '/single_add_robot'
    // }
  ]
}

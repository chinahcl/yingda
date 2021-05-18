export default {
  path: '/robot',
  component: () => import('@/views/Index_1'),
  name: 'robot',
  children: [
    {
      path: 'fa_piao_cha_yan',
      component: () => import('@/views/robot/fa_piao_cha_yan.vue'),
      name: 'fa_piao_cha_yan'
    },
    {
      path: 'fa_piao_shi_bie',
      component: () => import('@/views/robot/fa_piao_shi_bie.vue'),
      name: 'fa_piao_shi_bie'
    },
    {
      path: 'test_video',
      component: () => import('@/views/robot/test_video.vue'),
      name: 'test_video'
    },
    {
      path: 'test_robot1',
      component: () => import('@/views/robot/test_robot1.vue'),
      name: 'test_robot1'
    }
  ]
}

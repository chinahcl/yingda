export default {
  path: '/index_2',
  component: () => import('@/views/Index_1'),
  name: 'index_2',
  children: [
    {
      path: 'batch_add_use',
      component: () => import('@/views/two_view/batch_add_use.vue'),
      name: 'batch_add_use'
    },
    {
      path: 'single_add_use',
      component: () => import('@/views/two_view/single_add_use.vue'),
      name: 'single_add_use'
    },
    {
      path: 'fronzen_use',
      component: () => import('@/views/two_view/fronzen_use.vue'),
      name: 'fronzen_use'
    },
    {
      path: 'thaw_use',
      component: () => import('@/views/two_view/thaw_use.vue'),
      name: 'thaw_use'
    },
    {
      path: 'query_use',
      component: () => import('@/views/two_view/query_use.vue'),
      name: 'query_use'
    },
    {
      path: 'change_use',
      component: () => import('@/views/two_view/change_use.vue'),
      name: 'change_use'
    },
    {
      path: 'use_binding_robot',
      component: () => import('@/views/two_view/use_binding_robot.vue'),
      name: 'use_binding_robot'
    },
    {
      path: '/index_2',
      redirect: '/index_2/query_use'
    }
  ]
}

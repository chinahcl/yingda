export default {
  path: '/index_1',
  component: () => import('@/views/Index_1'),
  name: 'index_1',
  children: [
    {
      path: 'batch_add_unit',
      component: () => import('@/views/one_view/batch_add_unit.vue'),
      name: 'batch_add_unit'
    },
    {
      path: 'single_add_unit',
      component: () => import('@/views/one_view/single_add_unit.vue'),
      name: 'single_add_unit'
    },
    {
      path: 'fronzen_unit',
      component: () => import('@/views/one_view/fronzen_unit.vue'),
      name: 'fronzen_unit'
    },
    {
      path: 'thaw_unit',
      component: () => import('@/views/one_view/thaw_unit.vue'),
      name: 'thaw_unit'
    },
    {
      path: 'query_unit',
      component: () => import('@/views/one_view/query_unit.vue'),
      name: 'query_unit'
    },
    {
      path: 'change_unit',
      component: () => import('@/views/one_view/change_unit.vue'),
      name: 'change_unit'
    },
    {
      path: 'index',
      component: () => import('@/views/one_view/'),
      name: 'index'
    },
    {
      path: 'unit_binding_robot',
      component: () => import('@/views/one_view/unit_binding_robot'),
      name: 'unit_binding_robot'
    },
    {
      path: '/index_1',
      redirect: '/index_1/index'
    }
  ]
}

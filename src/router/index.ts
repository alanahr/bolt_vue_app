import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/positions'
    },
    {
      path: '/entities',
      component: () => import('../pages/entities/EntityList.vue')
    },
    {
      path: '/entities/new',
      component: () => import('../pages/entities/EntityEdit.vue')
    },
    {
      path: '/entities/:id',
      component: () => import('../pages/entities/EntityView.vue')
    },
    {
      path: '/entities/:id/edit',
      component: () => import('../pages/entities/EntityEdit.vue')
    },
    {
      path: '/positions',
      component: () => import('../pages/positions/PositionList.vue')
    },
    {
      path: '/positions/new',
      component: () => import('../pages/positions/PositionForm.vue')
    },
    {
      path: '/positions/:id',
      component: () => import('../pages/positions/PositionView.vue')
    },
    {
      path: '/positions/:id/edit',
      component: () => import('../pages/positions/PositionForm.vue')
    }
  ]
});

export default router;
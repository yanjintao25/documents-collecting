import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'DocumentList',
    component: () => import('@/views/DocumentList.vue'),
    meta: {
      title: '文档列表',
    },
  },
  {
    path: '/upload',
    name: 'DocumentUpload',
    component: () => import('@/views/DocumentUpload.vue'),
    meta: {
      title: '上传文档',
    },
  },
  {
    path: '/tags',
    name: 'TagManagement',
    component: () => import('@/views/TagManagement.vue'),
    meta: {
      title: '标签管理',
    },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - ${import.meta.env.VITE_APP_TITLE || '文档管理系统'}`
  }
  next()
})

export default router


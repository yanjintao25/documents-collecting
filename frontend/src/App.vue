<template>
  <el-container class="app-container">
    <el-header class="app-header">
      <div class="header-content">
        <h1>📄 {{ appTitle }}</h1>
        <el-menu
          mode="horizontal"
          :default-active="activeIndex"
          router
          class="header-menu"
        >
          <el-menu-item index="/">文档列表</el-menu-item>
          <el-menu-item index="/upload">上传文档</el-menu-item>
          <el-menu-item index="/tags">标签管理</el-menu-item>
        </el-menu>
      </div>
    </el-header>
    <el-main class="app-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeIndex = computed(() => route.path)
const appTitle = import.meta.env.VITE_APP_TITLE || '文档管理系统'
</script>

<style scoped>
.app-container {
  height: 100vh;
}

.app-header {
  background-color: #409eff;
  color: white;
  padding: 0;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.header-content h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 500;
}

.header-menu {
  background-color: transparent;
  border: none;
}

.header-menu :deep(.el-menu-item) {
  color: white;
}

.header-menu :deep(.el-menu-item.is-active) {
  color: #409eff;
  background-color: white;
}

.app-main {
  padding: 20px;
  background-color: #f5f5f5;
  min-height: calc(100vh - 60px);
  overflow-y: auto;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>


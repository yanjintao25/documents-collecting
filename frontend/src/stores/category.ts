import { defineStore } from 'pinia'
import { ref } from 'vue'
import { categoryApi } from '@/api/categories'
import type { Category } from '@/types/category'

export const useCategoryStore = defineStore('category', () => {
  const categories = ref<Category[]>([])
  const loading = ref(false)

  /**
   * 获取所有分类
   */
  const fetchCategories = async () => {
    loading.value = true
    try {
      const data = await categoryApi.getCategories()
      categories.value = data
    } finally {
      loading.value = false
    }
  }

  /**
   * 刷新分类列表
   */
  const refreshCategories = () => {
    return fetchCategories()
  }

  return {
    categories,
    loading,
    fetchCategories,
    refreshCategories,
  }
})

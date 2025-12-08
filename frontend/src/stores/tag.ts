import { defineStore } from 'pinia'
import { ref } from 'vue'
import { tagApi } from '@/api/tags'
import type { Tag } from '@/types/tag'

export const useTagStore = defineStore('tag', () => {
  const tags = ref<Tag[]>([])
  const loading = ref(false)

  /**
   * 获取所有标签
   */
  const fetchTags = async () => {
    loading.value = true
    try {
      const data = await tagApi.getTags()
      tags.value = data
    } finally {
      loading.value = false
    }
  }

  /**
   * 刷新标签列表
   */
  const refreshTags = () => {
    return fetchTags()
  }

  return {
    tags,
    loading,
    fetchTags,
    refreshTags,
  }
})


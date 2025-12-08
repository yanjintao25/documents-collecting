import { defineStore } from 'pinia'
import { ref } from 'vue'
import { documentApi } from '@/api/documents'
import type { Document } from '@/types/document'

export const useDocumentStore = defineStore('document', () => {
  const documents = ref<Document[]>([])
  const loading = ref(false)

  /**
   * 获取文档列表
   */
  const fetchDocuments = async (params?: { skip?: number; limit?: number }) => {
    loading.value = true
    try {
      const data = await documentApi.getDocuments(params)
      documents.value = data
    } finally {
      loading.value = false
    }
  }

  /**
   * 刷新文档列表
   */
  const refreshDocuments = () => {
    return fetchDocuments()
  }

  return {
    documents,
    loading,
    fetchDocuments,
    refreshDocuments,
  }
})


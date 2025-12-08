import request from '@/utils/request'
import type { Document, DocumentCreate, DocumentUpdate } from '@/types/document'

/**
 * 文档 API
 */
export const documentApi = {
  /**
   * 获取文档列表
   */
  getDocuments: (params?: { skip?: number; limit?: number }) => {
    return request.get<Document[]>('/v1/documents/', { params })
  },

  /**
   * 获取单个文档
   */
  getDocument: (id: number) => {
    return request.get<Document>(`/v1/documents/${id}`)
  },

  /**
   * 上传文档
   */
  uploadDocument: (formData: FormData) => {
    return request.post<Document>('/v1/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  /**
   * 更新文档
   */
  updateDocument: (id: number, data: DocumentUpdate) => {
    return request.put<Document>(`/v1/documents/${id}`, data)
  },

  /**
   * 删除文档
   */
  deleteDocument: (id: number) => {
    return request.delete(`/v1/documents/${id}`)
  },

  /**
   * 下载文档
   */
  downloadDocument: (id: number) => {
    return request.get(`/v1/documents/${id}/download`, {
      responseType: 'blob',
    })
  },
}


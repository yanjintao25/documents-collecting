import request from '@/utils/request'
import type { Tag, TagCreate, TagUpdate } from '@/types/tag'

/**
 * 标签 API
 */
export const tagApi = {
  /**
   * 获取所有标签
   */
  getTags: () => {
    return request.get<Tag[]>('/v1/tags/')
  },

  /**
   * 获取单个标签
   */
  getTag: (id: number) => {
    return request.get<Tag>(`/v1/tags/${id}`)
  },

  /**
   * 创建标签
   */
  createTag: (data: TagCreate) => {
    return request.post<Tag>('/v1/tags/', data)
  },

  /**
   * 更新标签
   */
  updateTag: (id: number, data: TagUpdate) => {
    return request.put<Tag>(`/v1/tags/${id}`, data)
  },

  /**
   * 删除标签
   */
  deleteTag: (id: number) => {
    return request.delete(`/v1/tags/${id}`)
  },
}


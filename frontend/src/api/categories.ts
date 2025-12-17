import request from '@/utils/request'
import type { Category } from '@/types/category'

/**
 * 分类 API
 */
export const categoryApi = {
  /**
   * 获取所有分类
   */
  getCategories: () => {
    return request.get<Category[]>('/v1/categories/')
  },
}

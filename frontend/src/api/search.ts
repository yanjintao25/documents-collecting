import request from '@/utils/request'
import type { Document } from '@/types/document'
import type { SearchParams } from '@/types/search'

/**
 * 搜索 API
 */
export const searchApi = {
  /**
   * 搜索文档
   */
  searchDocuments: (params: SearchParams) => {
    const queryParams: Record<string, any> = {}
    
    if (params.keyword) {
      queryParams.keyword = params.keyword
    }
    
    if (params.tag_ids && params.tag_ids.length > 0) {
      queryParams.tag_ids = params.tag_ids.join(',')
    }
    
    if (params.file_type) {
      queryParams.file_type = params.file_type
    }
    
    return request.get<Document[]>('/v1/search/', { params: queryParams })
  },
}


/**
 * 通用类型定义
 */

export interface ApiResponse<T = any> {
  data: T
  message?: string
  code?: number
}

export interface PaginationParams {
  page?: number
  pageSize?: number
  skip?: number
  limit?: number
}

export interface PaginationResponse<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
}


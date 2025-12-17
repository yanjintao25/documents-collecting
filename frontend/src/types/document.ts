import { Tag } from './tag'

/**
 * 文档类型定义
 */
export interface Document {
  id: number
  title: string
  file_size: number
  file_type: string
  pdf_file_size: number
  introduction: string | null
  write_time: string | null
  status: number
  upload_user_name: string
  upload_user_id: string
  update_user_name: string | null
  update_user_id: string | null
  category_id: number | null
  category_name: string | null
  create_time: string
  update_time: string
  description: string | null
  tags: Tag[]
}

export interface DocumentCreate {
  description?: string
  tag_ids?: number[]
}

export interface DocumentUpdate {
  description?: string
  tag_ids?: number[]
}


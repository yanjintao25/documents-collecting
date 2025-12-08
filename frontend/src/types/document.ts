import { Tag } from './tag'

/**
 * 文档类型定义
 */
export interface Document {
  id: number
  filename: string
  original_filename: string
  file_path: string
  file_size: number
  file_type: string
  description: string | null
  upload_time: string
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


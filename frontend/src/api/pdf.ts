import request from '@/utils/request'
import type { PDFGenerateRequest } from '@/types/pdf'

/**
 * PDF API
 */
export const pdfApi = {
  /**
   * 生成 PDF 汇编
   */
  generatePDF: (data: PDFGenerateRequest) => {
    return request.post('/v1/pdf/generate', data, {
      responseType: 'blob',
    })
  },
}


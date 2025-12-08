<template>
  <div class="document-list">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>文档列表</span>
          <el-button type="primary" @click="$router.push('/upload')">
            <el-icon><Plus /></el-icon>
            上传文档
          </el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索文档名称或描述"
          clearable
          style="width: 300px"
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>

        <el-select
          v-model="selectedTags"
          multiple
          placeholder="选择标签"
          style="width: 300px; margin-left: 10px"
          @change="handleSearch"
        >
          <el-option
            v-for="tag in tags"
            :key="tag.id"
            :label="tag.name"
            :value="tag.id"
          >
            <el-tag :color="tag.color" style="color: white">
              {{ tag.name }}
            </el-tag>
          </el-option>
        </el-select>

        <el-button type="primary" @click="handleSearch" style="margin-left: 10px">
          搜索
        </el-button>
        <el-button @click="resetSearch">重置</el-button>
      </div>

      <!-- 文档列表 -->
      <el-table
        :data="documents"
        style="width: 100%; margin-top: 20px"
        v-loading="loading"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="original_filename" label="文件名" min-width="200" />
        <el-table-column label="标签" width="200">
          <template #default="{ row }">
            <el-tag
              v-for="tag in row.tags"
              :key="tag.id"
              :color="tag.color"
              style="color: white; margin-right: 5px"
            >
              {{ tag.name }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="file_size" label="大小" width="120">
          <template #default="{ row }">
            {{ formatFileSize(row.file_size) }}
          </template>
        </el-table-column>
        <el-table-column prop="upload_time" label="上传时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.upload_time) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleDownload(row)">
              下载
            </el-button>
            <el-button type="warning" size="small" @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 批量操作 -->
      <div class="batch-actions" v-if="selectedDocuments.length > 0">
        <el-button type="success" @click="handleGeneratePDF">
          生成汇编 PDF ({{ selectedDocuments.length }})
        </el-button>
      </div>
    </el-card>

    <!-- 编辑对话框 -->
    <el-dialog v-model="editDialogVisible" title="编辑文档" width="500px">
      <el-form :model="editForm" label-width="80px">
        <el-form-item label="描述">
          <el-input
            v-model="editForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入文档描述"
          />
        </el-form-item>
        <el-form-item label="标签">
          <el-select
            v-model="editForm.tag_ids"
            multiple
            placeholder="选择标签"
            style="width: 100%"
          >
            <el-option
              v-for="tag in tags"
              :key="tag.id"
              :label="tag.name"
              :value="tag.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSaveEdit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import { documentApi } from '@/api/documents'
import { tagApi } from '@/api/tags'
import { searchApi } from '@/api/search'
import { pdfApi } from '@/api/pdf'
import { useTagStore } from '@/stores/tag'
import { formatFileSize, formatDateTime } from '@/utils/format'
import type { Document } from '@/types/document'

const documents = ref<Document[]>([])
const tags = ref(useTagStore().tags)
const loading = ref(false)
const searchKeyword = ref('')
const selectedTags = ref<number[]>([])
const selectedDocuments = ref<number[]>([])
const editDialogVisible = ref(false)
const editForm = ref({
  id: 0,
  description: '',
  tag_ids: [] as number[],
})

const tagStore = useTagStore()

// 加载文档列表
const loadDocuments = async () => {
  loading.value = true
  try {
    const data = await documentApi.getDocuments()
    documents.value = data
  } catch (error) {
    ElMessage.error('加载文档列表失败')
  } finally {
    loading.value = false
  }
}

// 加载标签列表
const loadTags = async () => {
  await tagStore.fetchTags()
  tags.value = tagStore.tags
}

// 搜索
const handleSearch = async () => {
  loading.value = true
  try {
    const data = await searchApi.searchDocuments({
      keyword: searchKeyword.value || undefined,
      tag_ids: selectedTags.value.length > 0 ? selectedTags.value : undefined,
    })
    documents.value = data
  } catch (error) {
    ElMessage.error('搜索失败')
  } finally {
    loading.value = false
  }
}

// 重置搜索
const resetSearch = () => {
  searchKeyword.value = ''
  selectedTags.value = []
  loadDocuments()
}

// 处理表格选择变化
const handleSelectionChange = (selection: Document[]) => {
  selectedDocuments.value = selection.map((doc) => doc.id)
}

// 下载文档
const handleDownload = async (doc: Document) => {
  try {
    const blob = await documentApi.downloadDocument(doc.id)
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = doc.original_filename
    link.click()
    window.URL.revokeObjectURL(url)
    ElMessage.success('下载成功')
  } catch (error) {
    ElMessage.error('下载失败')
  }
}

// 编辑文档
const handleEdit = (doc: Document) => {
  editForm.value = {
    id: doc.id,
    description: doc.description || '',
    tag_ids: doc.tags.map((t) => t.id),
  }
  editDialogVisible.value = true
}

// 保存编辑
const handleSaveEdit = async () => {
  try {
    await documentApi.updateDocument(editForm.value.id, {
      description: editForm.value.description,
      tag_ids: editForm.value.tag_ids,
    })
    ElMessage.success('更新成功')
    editDialogVisible.value = false
    loadDocuments()
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

// 删除文档
const handleDelete = async (doc: Document) => {
  try {
    await ElMessageBox.confirm('确定要删除这个文档吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await documentApi.deleteDocument(doc.id)
    ElMessage.success('删除成功')
    loadDocuments()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 生成 PDF
const handleGeneratePDF = async () => {
  if (selectedDocuments.value.length === 0) {
    ElMessage.warning('请先选择文档')
    return
  }

  try {
    const blob = await pdfApi.generatePDF({
      document_ids: selectedDocuments.value,
      title: '文档汇编',
    })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `文档汇编_${new Date().getTime()}.pdf`
    link.click()
    window.URL.revokeObjectURL(url)
    ElMessage.success('PDF 生成成功')
    selectedDocuments.value = []
  } catch (error) {
    ElMessage.error('PDF 生成失败')
  }
}

onMounted(() => {
  loadDocuments()
  loadTags()
})
</script>

<style scoped>
.document-list {
  max-width: 1400px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-bar {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.batch-actions {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}
</style>


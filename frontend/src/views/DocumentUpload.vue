<template>
  <div class="document-upload">
    <el-card shadow="hover">
      <template #header>
        <span>上传文档</span>
      </template>

      <el-upload
        class="upload-demo"
        drag
        :auto-upload="false"
        :on-change="handleFileChange"
        :file-list="fileList"
        multiple
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          将文件拖到此处，或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            支持上传各种格式的文档文件
          </div>
        </template>
      </el-upload>

      <el-form
        label-width="100px"
        style="margin-top: 20px"
        v-for="(file, index) in fileList"
        :key="index"
      >
        <el-divider v-if="index > 0" />
        <h4>{{ file.name }}</h4>
        <el-form-item label="描述">
          <el-input
            v-model="file.description"
            type="textarea"
            :rows="2"
            placeholder="请输入文档描述（可选）"
          />
        </el-form-item>
        <el-form-item label="分类">
          <el-select
            v-model="file.category_id"
            placeholder="选择分类（可选）"
            style="width: 100%"
          >
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
        </el-form-item>
      </el-form>

      <div class="upload-actions">
        <el-button @click="$router.push('/')">取消</el-button>
        <el-button type="primary" @click="handleUpload" :loading="uploading">
          上传
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'
import { documentApi } from '@/api/documents'
import { useCategoryStore } from '@/stores/category'
import type { UploadFile, UploadFiles } from 'element-plus'
import type { Category } from '@/types/category'

interface FileItem extends UploadFile {
  description?: string
  category_id?: number
}

const fileList = ref<FileItem[]>([])
const categories = ref<Category[]>([])
const uploading = ref(false)

const categoryStore = useCategoryStore()

// 文件变化处理
const handleFileChange = (_file: UploadFile, files: UploadFiles) => {
  fileList.value = files.map((f) => ({
    ...f,
    description: '',
    category_id: undefined,
  }))
}

// 加载分类
const loadCategories = async () => {
  await categoryStore.fetchCategories()
  categories.value = categoryStore.categories
}

// 上传文件
const handleUpload = async () => {
  if (fileList.value.length === 0) {
    ElMessage.warning('请先选择文件')
    return
  }

  uploading.value = true

  try {
    const uploadPromises = fileList.value.map(async (file) => {
      const formData = new FormData()
      formData.append('file', file.raw!)
      if (file.description) {
        formData.append('description', file.description)
      }
      if (file.category_id !== undefined && file.category_id !== null) {
        formData.append('category_id', file.category_id.toString())
      }
      return documentApi.uploadDocument(formData)
    })

    await Promise.all(uploadPromises)
    ElMessage.success('上传成功')
    fileList.value = []
    // 跳转到文档列表
    setTimeout(() => {
      window.location.href = '/'
    }, 1000)
  } catch (error) {
    ElMessage.error('上传失败')
  } finally {
    uploading.value = false
  }
}

onMounted(() => {
  loadCategories()
})
</script>

<style scoped>
.document-upload {
  max-width: 800px;
  margin: 0 auto;
}

.upload-demo {
  width: 100%;
}

.upload-actions {
  margin-top: 20px;
  text-align: right;
}
</style>


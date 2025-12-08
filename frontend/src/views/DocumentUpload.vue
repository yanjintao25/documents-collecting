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
        :model="form"
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
        <el-form-item label="标签">
          <el-select
            v-model="file.tag_ids"
            multiple
            placeholder="选择标签（可选）"
            style="width: 100%"
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
import { useTagStore } from '@/stores/tag'
import type { UploadFile, UploadFiles } from 'element-plus'
import type { Tag } from '@/types/tag'

interface FileItem extends UploadFile {
  description?: string
  tag_ids?: number[]
}

const fileList = ref<FileItem[]>([])
const tags = ref<Tag[]>([])
const uploading = ref(false)

const tagStore = useTagStore()

// 文件变化处理
const handleFileChange = (file: UploadFile, files: UploadFiles) => {
  fileList.value = files.map((f) => ({
    ...f,
    description: '',
    tag_ids: [] as number[],
  }))
}

// 加载标签
const loadTags = async () => {
  await tagStore.fetchTags()
  tags.value = tagStore.tags
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
      if (file.tag_ids && file.tag_ids.length > 0) {
        formData.append('tag_ids', file.tag_ids.join(','))
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
  loadTags()
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


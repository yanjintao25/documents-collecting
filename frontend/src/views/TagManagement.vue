<template>
  <div class="tag-management">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>标签管理</span>
          <el-button type="primary" @click="handleAddTag">
            <el-icon><Plus /></el-icon>
            添加标签
          </el-button>
        </div>
      </template>

      <el-table :data="tags" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="标签名称" width="200">
          <template #default="{ row }">
            <el-tag :color="row.color" style="color: white">
              {{ row.name }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="color" label="颜色" width="150">
          <template #default="{ row }">
            <el-color-picker
              v-model="row.color"
              @change="handleColorChange(row)"
            />
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑标签对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="标签名称" required>
          <el-input v-model="form.name" placeholder="请输入标签名称" />
        </el-form-item>
        <el-form-item label="标签颜色">
          <el-color-picker v-model="form.color" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { tagApi } from '@/api/tags'
import { useTagStore } from '@/stores/tag'
import { formatDateTime } from '@/utils/format'
import type { Tag, TagCreate } from '@/types/tag'

const tagStore = useTagStore()
const tags = ref<Tag[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const form = ref<TagCreate>({
  name: '',
  color: '#409EFF',
})
const currentTagId = ref(0)

const dialogTitle = computed(() => (isEdit.value ? '编辑标签' : '添加标签'))

// 加载标签列表
const loadTags = async () => {
  loading.value = true
  try {
    await tagStore.fetchTags()
    tags.value = tagStore.tags
  } catch (error) {
    ElMessage.error('加载标签列表失败')
  } finally {
    loading.value = false
  }
}

// 添加标签
const handleAddTag = () => {
  isEdit.value = false
  form.value = {
    name: '',
    color: '#409EFF',
  }
  dialogVisible.value = true
}

// 编辑标签
const handleEdit = (tag: Tag) => {
  isEdit.value = true
  currentTagId.value = tag.id
  form.value = {
    name: tag.name,
    color: tag.color,
  }
  dialogVisible.value = true
}

// 保存标签
const handleSave = async () => {
  if (!form.value.name.trim()) {
    ElMessage.warning('请输入标签名称')
    return
  }

  try {
    if (isEdit.value) {
      await tagApi.updateTag(currentTagId.value, form.value)
      ElMessage.success('更新成功')
    } else {
      await tagApi.createTag(form.value)
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    await loadTags()
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '操作失败')
  }
}

// 删除标签
const handleDelete = async (tag: Tag) => {
  try {
    await ElMessageBox.confirm('确定要删除这个标签吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await tagApi.deleteTag(tag.id)
    ElMessage.success('删除成功')
    await loadTags()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 颜色变化处理
const handleColorChange = async (tag: Tag) => {
  try {
    await tagApi.updateTag(tag.id, {
      name: tag.name,
      color: tag.color,
    })
    ElMessage.success('颜色更新成功')
  } catch (error) {
    ElMessage.error('颜色更新失败')
    await loadTags() // 重新加载以恢复原值
  }
}

onMounted(() => {
  loadTags()
})
</script>

<style scoped>
.tag-management {
  max-width: 1000px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>


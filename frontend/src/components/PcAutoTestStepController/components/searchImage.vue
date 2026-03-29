<template>
  <div class="search-image">
    <div
        v-if="treeImageList.length === 0"
        style="padding: 12px; text-align: center; color: #c0c4cc; font-size: 13px;"
    >
      {{ filterText ? '暂无匹配素材' : '请输入素材名称搜索' }}
    </div>

    <div
        v-for="treeImage in treeImageList"
        :key="treeImage.tree_id || treeImage.tree_name"
        class="si-group"
    >
      <div class="si-group-label">{{ treeImage.tree_name }}</div>
      <div class="si-grid">
        <div
            v-for="(pic, picIdx) in treeImage.picture_data"
            :key="pic.id"
            class="si-item"
        >
          <el-image
              :src="pic.file_path || pic.url || pic.image_url || ''"
              fit="contain"
              class="si-thumb"
              @click="emitPreview(treeImage, picIdx)"
          >
            <template #placeholder>
              <el-icon><Loading /></el-icon>
            </template>
            <template #error>
              <el-icon><Picture /></el-icon>
            </template>
          </el-image>
          <div class="si-name" :title="pic.name">{{ pic.name }}</div>
          <el-button
              type="primary"
              size="small"
              class="si-use-btn"
              @click.stop="handleUseImage(pic)"
          >
            <el-icon><Check /></el-icon>选用
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, toRef, watch } from 'vue'
import { usePcPictureApi } from '/@/api/usePcAutoApi/pcPicture.js'
import { ElMessage } from 'element-plus'
import { Picture, Loading, Check } from '@element-plus/icons-vue'

const props = defineProps({
  filterText: { type: String, default: '' },
})
const emit = defineEmits(['preview-request', 'use-image'])

const treeImageList = ref([])

const filterTextRef = toRef(props, 'filterText')

watch(filterTextRef, async (text) => {
  if (!text) {
    treeImageList.value = []
    return
  }
  try {
    const res = await usePcPictureApi().pictureByName({ picture_name: text })
    treeImageList.value = res.data || []
  } catch {
    ElMessage.error('素材搜索失败')
    treeImageList.value = []
  }
})

function emitPreview(treeImage, picIdx) {
  const list = []
  let globalIndex = 0
  let targetIndex = 0

  for (const group of treeImageList.value) {
    for (let i = 0; i < (group.picture_data || []).length; i++) {
      const pic = group.picture_data[i]
      const url = pic.file_path || pic.url || pic.image_url || ''
      list.push(url)
      if (group === treeImage && i === picIdx) {
        targetIndex = globalIndex
      }
      globalIndex++
    }
  }

  emit('preview-request', { list, index: targetIndex })
}

function handleUseImage(pic) {
  const url = pic.file_path || pic.url || pic.image_url || ''
  emit('use-image', url)
}
</script>

<style lang="scss" scoped>
.search-image {
  max-height: 300px;
  overflow-y: auto;
  margin-top: 8px;
}

.si-group {
  margin-bottom: 8px;
}

.si-group-label {
  font-size: 12px;
  color: #909399;
  padding: 4px 0 2px;
  border-bottom: 1px solid #f0f0f0;
  margin-bottom: 6px;
}

.si-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.si-item {
  width: 90px;
  text-align: center;
  cursor: pointer;

  &:hover .si-use-btn {
    opacity: 1;
  }
}

.si-thumb {
  width: 80px;
  height: 60px;
  border: 1px solid #eee;
  border-radius: 4px;
}

.si-name {
  font-size: 11px;
  color: #606266;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-top: 2px;
}

.si-use-btn {
  opacity: 0;
  transition: opacity 0.2s;
  margin-top: 2px;
  width: 100%;
}
</style>

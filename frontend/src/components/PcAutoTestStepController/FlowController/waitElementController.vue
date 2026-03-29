<template>
  <div class="wait-element-controller">
    <div class="wec-row">
      <!-- 左侧：操作类型中文名 -->
      <div class="wec-type-label">
        {{ operationTypeToZh[data.request.comparator] || data.request.comparator }}
      </div>

      <!-- 图片区域 -->
      <div class="wec-image-area">
        <!-- 素材库模式 -->
        <template v-if="data.request.picture_is_search">
          <el-popover
              v-model:visible="popoverVisible"
              placement="bottom"
              :width="440"
              trigger="manual"
              :teleported="false"
          >
            <template #reference>
              <div class="wec-image-trigger" @click="openPopover">
                <el-image
                    v-if="data.request.image"
                    :src="data.request.image"
                    fit="contain"
                    class="wec-thumb"
                    @click.stop="previewSingle(data.request.image)"
                />
                <div v-else class="wec-placeholder">点击选择素材</div>
              </div>
            </template>
            <el-input
                v-model="imageFilterText"
                placeholder="搜索素材名称"
                clearable
                size="small"
                @input="onImageFilterInput"
            />
            <SearchImage
                :filterText="imageFilterText"
                @use-image="handleUseImage"
                @preview-request="handlePreviewRequest"
            />
          </el-popover>
        </template>

        <!-- 粘贴模式 -->
        <template v-else>
          <div
              class="wec-paste-area"
              tabindex="0"
              @paste="handlePaste($event, 'image')"
          >
            <el-image
                v-if="data.request.image"
                :src="data.request.image"
                fit="contain"
                class="wec-thumb"
                @click="previewSingle(data.request.image)"
            />
            <div v-else class="wec-placeholder">点此区域 Ctrl+V 粘贴截图</div>
          </div>
        </template>
      </div>

      <!-- 素材库 / 粘贴 开关 -->
      <el-switch
          v-model="data.request.picture_is_search"
          active-text="素材库"
          inactive-text="粘贴"
          inline-prompt
      />

      <!-- 追踪类型 -->
      <el-select
          v-model="data.request.waitElementType"
          size="small"
          style="width: 130px; flex-shrink: 0;"
          placeholder="追踪类型"
      >
        <el-option
            v-for="opt in waitElementTypeOptions"
            :key="opt.value"
            :label="opt.label"
            :value="opt.value"
        />
      </el-select>

      <!-- 等待时间 -->
      <el-input-number
          v-model="data.request.wait_time"
          :min="1"
          :max="300"
          size="small"
          style="width: 100px; flex-shrink: 0;"
      />
    </div>

    <!-- 图片全屏预览 -->
    <el-image-viewer
        v-if="showViewer"
        :url-list="previewList"
        :initial-index="currentIndex"
        teleported
        @close="handleClosePreview"
    />
  </div>
</template>

<script setup name="waitElementController">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import useVModel from '/@/utils/useVModel'
import useMouseData from '/@/hooks/pcAutoTest/useMouseData.js'
import { usePcFileManagerApi } from '/@/api/usePcAutoApi/pcFileManager.js'
import SearchImage from '../components/searchImage.vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  data: { type: Object, required: true },
})
const emit = defineEmits(['update:data'])
const data = useVModel(props, 'data', emit)

const { operationTypeToZh } = useMouseData()

const waitElementTypeOptions = [
  { value: 'wait_appear',    label: '等待元素出现' },
  { value: 'wait_disappear', label: '等待元素消失' },
]

const popoverVisible = ref(false)
const dragImagePopoverVisible = ref(false)
const showViewer = ref(false)
const previewList = ref([])
const currentIndex = ref(0)
const imageFilterText = ref('')
const dragImageFilterText = ref('')

function useDebounceFn(fn, delay = 300) {
  let timer = null
  return (...args) => {
    clearTimeout(timer)
    timer = setTimeout(() => fn(...args), delay)
  }
}

function createDebounceHandler(fn, delay = 300) {
  return useDebounceFn(fn, delay)
}

function handleEsc(e) {
  if (e.key !== 'Escape') return
  if (showViewer.value) {
    handleClosePreview()
  } else {
    popoverVisible.value = false
    dragImagePopoverVisible.value = false
  }
}

onMounted(() => window.addEventListener('keydown', handleEsc))
onBeforeUnmount(() => window.removeEventListener('keydown', handleEsc))

const openPopover = createDebounceHandler(() => {
  popoverVisible.value = true
}, 200)

function onImageFilterInput(val) {
  if (!val) popoverVisible.value = false
}

function onDragImageFilterInput(val) {
  if (!val) dragImagePopoverVisible.value = false
}

function handleUseImage(image_url) {
  data.value.request.image = image_url
  popoverVisible.value = false
  imageFilterText.value = ''
}

function handleUseDragImage(image_url) {
  data.value.request.dragImage = image_url
  dragImagePopoverVisible.value = false
  dragImageFilterText.value = ''
}

function handlePreviewRequest(payload) {
  previewList.value = payload.list
  currentIndex.value = payload.index
  showViewer.value = true
}

function handleClosePreview() {
  showViewer.value = false
  previewList.value = []
  currentIndex.value = 0
}

function previewSingle(url) {
  if (!url) return
  previewList.value = [url]
  currentIndex.value = 0
  showViewer.value = true
}

async function handlePaste(event, target = 'image') {
  const items = event.clipboardData?.items
  if (!items) return
  for (const item of items) {
    if (item.type.startsWith('image/')) {
      const file = item.getAsFile()
      if (!file) continue
      const formData = new FormData()
      formData.append('file', file)
      try {
        const res = await usePcFileManagerApi().uploadPhoto(formData)
        const url = res.data?.file_path || res.data?.url || ''
        if (target === 'dragImage') {
          data.value.request.dragImage = url
        } else {
          data.value.request.image = url
        }
        ElMessage.success('图片上传成功')
      } catch {
        ElMessage.error('图片上传失败')
      }
      break
    }
  }
}
</script>

<style lang="scss" scoped>
.wait-element-controller {
  padding: 4px 0;
}

.wec-row {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.wec-type-label {
  font-size: 13px;
  color: #606266;
  flex-shrink: 0;
  min-width: 60px;
}

.wec-image-area {
  flex: 1;
  min-width: 100px;
}

.wec-image-trigger,
.wec-paste-area {
  border: 1px dashed #d9d9d9;
  border-radius: 4px;
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  padding: 4px;
  outline: none;
  transition: border-color 0.2s;

  &:hover,
  &:focus {
    border-color: #409eff;
  }
}

.wec-thumb {
  max-width: 120px;
  max-height: 80px;
}

.wec-placeholder {
  color: #c0c4cc;
  font-size: 12px;
  text-align: center;
  padding: 4px;
}
</style>

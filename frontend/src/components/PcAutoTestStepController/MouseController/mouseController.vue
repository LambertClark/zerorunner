<template>
  <div class="mouse-controller">
    <div class="mc-row">
      <!-- 左侧：操作类型中文名 -->
      <div class="mc-type-label">
        {{ operationTypeToZh[data.request.comparator] || data.request.comparator }}
      </div>

      <!-- 主图片区域 -->
      <div class="mc-image-area">
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
              <div class="mc-image-trigger" @click="openPopover">
                <el-image
                    v-if="data.request.image"
                    :src="data.request.image"
                    fit="contain"
                    class="mc-thumb"
                    @click.stop="previewSingle(data.request.image)"
                />
                <div v-else class="mc-placeholder">点击选择素材</div>
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
              class="mc-paste-area"
              tabindex="0"
              @paste="handlePaste($event, 'image')"
          >
            <el-image
                v-if="data.request.image"
                :src="data.request.image"
                fit="contain"
                class="mc-thumb"
                @click="previewSingle(data.request.image)"
            />
            <div v-else class="mc-placeholder">点此区域 Ctrl+V 粘贴截图</div>
          </div>
        </template>
      </div>

      <!-- 素材库 / 粘贴 开关 -->
      <div class="mc-switch-area">
        <el-switch
            v-model="data.request.picture_is_search"
            active-text="素材库"
            inactive-text="粘贴"
            inline-prompt
        />
      </div>
    </div>

    <!-- 拖拽目标（仅 MOUSE_DRAG_ELEMENT_TO_ELEMENT） -->
    <template v-if="data.request.comparator === 'MOUSE_DRAG_ELEMENT_TO_ELEMENT'">
      <el-divider content-position="left" style="margin: 8px 0;">拖拽目标</el-divider>
      <div class="mc-row">
        <div class="mc-type-label">目标图片</div>

        <div class="mc-image-area">
          <template v-if="data.request.picture_is_search">
            <el-popover
                v-model:visible="dragImagePopoverVisible"
                placement="bottom"
                :width="440"
                trigger="manual"
                :teleported="false"
            >
              <template #reference>
                <div class="mc-image-trigger" @click="openDragPopover">
                  <el-image
                      v-if="data.request.dragImage"
                      :src="data.request.dragImage"
                      fit="contain"
                      class="mc-thumb"
                      @click.stop="previewSingle(data.request.dragImage)"
                  />
                  <div v-else class="mc-placeholder">点击选择目标素材</div>
                </div>
              </template>
              <el-input
                  v-model="dragImageFilterText"
                  placeholder="搜索目标素材名称"
                  clearable
                  size="small"
                  @input="onDragImageFilterInput"
              />
              <SearchImage
                  :filterText="dragImageFilterText"
                  @use-image="handleUseDragImage"
                  @preview-request="handlePreviewRequest"
              />
            </el-popover>
          </template>
          <template v-else>
            <div
                class="mc-paste-area"
                tabindex="0"
                @paste="handlePaste($event, 'dragImage')"
            >
              <el-image
                  v-if="data.request.dragImage"
                  :src="data.request.dragImage"
                  fit="contain"
                  class="mc-thumb"
                  @click="previewSingle(data.request.dragImage)"
              />
              <div v-else class="mc-placeholder">点此区域 Ctrl+V 粘贴目标截图</div>
            </div>
          </template>
        </div>
      </div>
    </template>

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

<script setup name="mouseController">
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

const popoverVisible = ref(false)
const dragImagePopoverVisible = ref(false)
const showViewer = ref(false)
const previewList = ref([])
const currentIndex = ref(0)
const imageFilterText = ref('')
const dragImageFilterText = ref('')

// 防抖工厂
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

// ESC 拦截：关闭预览或弹层
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

// 防抖打开弹层
const openPopover = createDebounceHandler(() => {
  popoverVisible.value = true
}, 200)

const openDragPopover = createDebounceHandler(() => {
  dragImagePopoverVisible.value = true
}, 200)

// 清空关键字时立即关闭弹层
function onImageFilterInput(val) {
  if (!val) popoverVisible.value = false
}

function onDragImageFilterInput(val) {
  if (!val) dragImagePopoverVisible.value = false
}

// 选用主图
function handleUseImage(image_url) {
  data.value.request.image = image_url
  popoverVisible.value = false
  imageFilterText.value = ''
}

// 选用拖拽目标图
function handleUseDragImage(image_url) {
  data.value.request.dragImage = image_url
  dragImagePopoverVisible.value = false
  dragImageFilterText.value = ''
}

// 接收子组件预览请求（多图列表）
function handlePreviewRequest(payload) {
  previewList.value = payload.list
  currentIndex.value = payload.index
  showViewer.value = true
}

// 关闭预览
function handleClosePreview() {
  showViewer.value = false
  previewList.value = []
  currentIndex.value = 0
}

// 单图预览
function previewSingle(url) {
  if (!url) return
  previewList.value = [url]
  currentIndex.value = 0
  showViewer.value = true
}

// 剪贴板粘贴上传
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
.mouse-controller {
  padding: 4px 0;
}

.mc-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.mc-type-label {
  font-size: 13px;
  color: #606266;
  flex-shrink: 0;
  min-width: 60px;
}

.mc-image-area {
  flex: 1;
  min-width: 100px;
}

.mc-image-trigger,
.mc-paste-area {
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

.mc-thumb {
  max-width: 120px;
  max-height: 80px;
}

.mc-placeholder {
  color: #c0c4cc;
  font-size: 12px;
  text-align: center;
  padding: 4px;
}

.mc-switch-area {
  flex-shrink: 0;
}
</style>

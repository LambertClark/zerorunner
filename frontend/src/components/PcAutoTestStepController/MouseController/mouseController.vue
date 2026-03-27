<template>
  <div class="mouse-controller">
    <el-form label-width="90px" size="small">

      <!-- 素材选择 -->
      <el-form-item label="目标素材">
        <el-input
            v-model="data.pc_request.image_name"
            placeholder="请输入素材名称搜索"
            clearable
            @input="searchPicture"
        >
          <template #append>
            <el-button @click="openPictureSelector">选择</el-button>
          </template>
        </el-input>
      </el-form-item>

      <!-- 素材预览 -->
      <el-form-item label="素材预览" v-if="data.pc_request.image_url">
        <el-image
            :src="imagePreviewUrl"
            fit="contain"
            style="width: 120px; height: 80px; border: 1px solid #ddd; border-radius: 4px;"
            :preview-src-list="[imagePreviewUrl]"
            preview-teleported
        />
      </el-form-item>

      <!-- 相似度阈值 -->
      <el-form-item label="相似度">
        <el-slider
            v-model="data.pc_request.threshold"
            :min="0.1"
            :max="1"
            :step="0.05"
            :format-tooltip="(v) => `${(v * 100).toFixed(0)}%`"
            show-input
            style="width: 100%"
        />
      </el-form-item>

      <!-- 超时时间 -->
      <el-form-item label="超时(s)">
        <el-input-number
            v-model="data.pc_request.timeout"
            :min="1"
            :max="120"
            style="width: 100%"
        />
      </el-form-item>

      <!-- 拖拽目标（仅 mouse_drag） -->
      <template v-if="data.step_type === 'mouse_drag'">
        <el-divider content-position="left">拖拽目标</el-divider>
        <el-form-item label="目标素材">
          <el-input
              v-model="data.pc_request.to_image_name"
              placeholder="请输入目标素材名称"
              clearable
              @input="searchTargetPicture"
          >
            <template #append>
              <el-button @click="openTargetPictureSelector">选择</el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="目标预览" v-if="data.pc_request.to_image_url">
          <el-image
              :src="targetImagePreviewUrl"
              fit="contain"
              style="width: 120px; height: 80px; border: 1px solid #ddd; border-radius: 4px;"
              :preview-src-list="[targetImagePreviewUrl]"
              preview-teleported
          />
        </el-form-item>
      </template>

      <!-- 滚动次数（scroll） -->
      <el-form-item
          label="滚动次数"
          v-if="data.step_type === 'mouse_scroll_wheel_down' || data.step_type === 'mouse_scroll_wheel_up'"
      >
        <el-input-number v-model="data.pc_request.scroll_times" :min="1" :max="50" style="width: 100%"/>
      </el-form-item>

    </el-form>

    <!-- 图片选择弹窗 -->
    <PictureSelectDialog
        v-if="state.showPictureDialog"
        v-model:visible="state.showPictureDialog"
        @select="handlePictureSelect"
    />
    <PictureSelectDialog
        v-if="state.showTargetPictureDialog"
        v-model:visible="state.showTargetPictureDialog"
        @select="handleTargetPictureSelect"
    />
  </div>
</template>

<script setup name="MouseController">
import { computed, reactive } from 'vue'
import { getBaseApiUrl } from '/@/utils/config'
import PictureSelectDialog from '/@/components/PcAutoTestStepController/PictureSelect/pictureSelectDialog.vue'

const props = defineProps({
  data: {
    type: Object,
    default: () => ({}),
  },
})

const emit = defineEmits(['update:data'])

const state = reactive({
  showPictureDialog: false,
  showTargetPictureDialog: false,
})

const imagePreviewUrl = computed(() => {
  const url = props.data.pc_request?.image_url
  if (!url) return ''
  return url.startsWith('http') ? url : `${getBaseApiUrl()}/${url}`
})

const targetImagePreviewUrl = computed(() => {
  const url = props.data.pc_request?.to_image_url
  if (!url) return ''
  return url.startsWith('http') ? url : `${getBaseApiUrl()}/${url}`
})

const openPictureSelector = () => {
  state.showPictureDialog = true
}

const openTargetPictureSelector = () => {
  state.showTargetPictureDialog = true
}

const searchPicture = () => {
  // 输入框变更时可触发搜索，弹窗内已有搜索逻辑，这里仅占位
}

const searchTargetPicture = () => {}

const handlePictureSelect = (picture) => {
  props.data.pc_request.image_id = picture.id
  props.data.pc_request.image_name = picture.name
  props.data.pc_request.image_url = picture.file_path || picture.url || ''
  state.showPictureDialog = false
}

const handleTargetPictureSelect = (picture) => {
  props.data.pc_request.to_image_id = picture.id
  props.data.pc_request.to_image_name = picture.name
  props.data.pc_request.to_image_url = picture.file_path || picture.url || ''
  state.showTargetPictureDialog = false
}
</script>

<style lang="scss" scoped>
.mouse-controller {
  padding: 0 4px;
}
</style>

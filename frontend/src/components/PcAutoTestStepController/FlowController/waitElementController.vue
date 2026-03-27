<template>
  <div class="wait-element-controller">
    <el-form label-width="90px" size="small">

      <el-form-item label="目标素材">
        <el-input
            v-model="data.pc_request.image_name"
            placeholder="请输入素材名称"
            clearable
        >
          <template #append>
            <el-button @click="state.showPictureDialog = true">选择</el-button>
          </template>
        </el-input>
      </el-form-item>

      <el-form-item label="素材预览" v-if="data.pc_request.image_url">
        <el-image
            :src="imagePreviewUrl"
            fit="contain"
            style="width: 120px; height: 80px; border: 1px solid #ddd; border-radius: 4px;"
            :preview-src-list="[imagePreviewUrl]"
            preview-teleported
        />
      </el-form-item>

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

      <el-form-item label="超时(s)">
        <el-input-number
            v-model="data.pc_request.timeout"
            :min="1"
            :max="300"
            style="width: 100%"
        />
      </el-form-item>

    </el-form>

    <PictureSelectDialog
        v-if="state.showPictureDialog"
        v-model:visible="state.showPictureDialog"
        @select="handlePictureSelect"
    />
  </div>
</template>

<script setup name="WaitElementController">
import { computed, reactive } from 'vue'
import { getBaseApiUrl } from '/@/utils/config'
import PictureSelectDialog from '/@/components/PcAutoTestStepController/PictureSelect/pictureSelectDialog.vue'

const props = defineProps({
  data: {
    type: Object,
    default: () => ({}),
  },
})

const state = reactive({
  showPictureDialog: false,
})

const imagePreviewUrl = computed(() => {
  const url = props.data.pc_request?.image_url
  if (!url) return ''
  return url.startsWith('http') ? url : `${getBaseApiUrl()}/${url}`
})

const handlePictureSelect = (picture) => {
  props.data.pc_request.image_id = picture.id
  props.data.pc_request.image_name = picture.name
  props.data.pc_request.image_url = picture.file_path || picture.url || ''
  state.showPictureDialog = false
}
</script>

<style lang="scss" scoped>
.wait-element-controller {
  padding: 0 4px;
}
</style>

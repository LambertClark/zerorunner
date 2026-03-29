<template>
  <div class="keyboard-controller">
    <div class="kc-row">
      <!-- 左侧：操作类型中文名 -->
      <span class="kc-type-label">
        {{ operationTypeToZh[data.request.comparator] || data.request.comparator }}
      </span>

      <!-- 仅 keyboard_input 显示文本输入框 -->
      <el-input
          v-if="data.request.comparator === operationTypeEnum.keyboard_input"
          v-model="data.request.text"
          type="textarea"
          :rows="2"
          placeholder="请输入要键入的文本内容"
          style="flex: 1;"
          @paste="handlePaste"
      />
    </div>
  </div>
</template>

<script setup name="keyboardController">
import useVModel from '/@/utils/useVModel'
import useMouseData from '/@/hooks/pcAutoTest/useMouseData.js'
import { usePcFileManagerApi } from '/@/api/usePcAutoApi/pcFileManager.js'

const props = defineProps({
  data: { type: Object, required: true },
})
const emit = defineEmits(['update:data'])
const data = useVModel(props, 'data', emit)

const { operationTypeToZh, operationTypeEnum } = useMouseData()

async function handlePaste(event) {
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
        data.value.request.image = url
      } catch {}
      break
    }
  }
}
</script>

<style lang="scss" scoped>
.keyboard-controller {
  padding: 4px 0;
}

.kc-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.kc-type-label {
  font-size: 13px;
  color: #606266;
  flex-shrink: 0;
  min-width: 60px;
}
</style>

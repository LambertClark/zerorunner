<template>
  <div class="keyboard-controller">
    <el-form label-width="90px" size="small">

      <!-- keyboard_input：文本输入 -->
      <el-form-item v-if="data.step_type === 'keyboard_input'" label="输入文本">
        <el-input
            v-model="data.pc_request.input_text"
            type="textarea"
            :rows="3"
            placeholder="请输入要键入的文本内容"
        />
      </el-form-item>

      <!-- keyboard_clear / keyboard_select_all / keyboard_enter：无额外参数 -->
      <el-form-item v-if="['keyboard_clear','keyboard_select_all','keyboard_enter'].includes(data.step_type)">
        <el-alert
            :title="`执行：${stepLabel}，无需额外参数`"
            type="info"
            :closable="false"
            show-icon
        />
      </el-form-item>

    </el-form>
  </div>
</template>

<script setup name="KeyboardController">
import { computed } from 'vue'
import { getPcStepLabel } from '/@/hooks/pcAutoTest/useMouseData.js'

const props = defineProps({
  data: {
    type: Object,
    default: () => ({}),
  },
})

const stepLabel = computed(() => getPcStepLabel(props.data.step_type))
</script>

<style lang="scss" scoped>
.keyboard-controller {
  padding: 0 4px;
}
</style>

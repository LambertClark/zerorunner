<template>
  <div class="pc-step-node" @click="$emit('node-click', data)">
    <el-card
        class="step-card w100"
        :class="[`pc-${data.step_type}-border`]"
    >
      <div class="step-header">
        <!-- 步骤类型标签 -->
        <el-tag
            size="small"
            :color="stepColor"
            style="color: #fff; border: none; margin-right: 8px; flex-shrink: 0;"
        >
          {{ stepLabel }}
        </el-tag>

        <!-- 步骤名称 -->
        <div class="step-header__content" style="flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
          <span>{{ data.name || stepLabel }}</span>
        </div>

        <!-- 操作区 -->
        <div class="step-header__right" @click.stop="">
          <el-tooltip content="启用/禁用" placement="top">
            <el-switch v-model="data.enable" inline-prompt size="small" style="margin-right: 6px"/>
          </el-tooltip>

          <el-button circle size="small" @click.stop="copyNode(data)">
            <el-icon><ele-DocumentCopy/></el-icon>
          </el-button>

          <el-button type="danger" circle size="small" @click.stop="deletedNode">
            <el-icon><ele-Delete/></el-icon>
          </el-button>
        </div>
      </div>

      <!-- 步骤摘要（只读预览） -->
      <div class="step-summary" v-if="summary">
        <el-text type="info" size="small" truncated>{{ summary }}</el-text>
      </div>
    </el-card>
  </div>
</template>

<script setup name="PcStepNode">
import { computed } from 'vue'
import { getPcStepLabel, operationTypeToZh, operationTypeEnum } from '/@/hooks/pcAutoTest/useMouseData.js'

const emit = defineEmits(['copy-node', 'deleted-node', 'node-click'])

const props = defineProps({
  data: {
    type: Object,
    default: () => ({}),
  },
  node: {
    type: Object,
    default: () => ({}),
  },
})

const stepLabel = computed(() => getPcStepLabel(props.data.step_type))

const stepColor = computed(() => {
  const colorMap = {
    mouse_left_click: '#409EFF',
    mouse_right_click: '#409EFF',
    mouse_double_click: '#409EFF',
    mouse_hover: '#409EFF',
    mouse_drag: '#409EFF',
    mouse_scroll_wheel_down: '#409EFF',
    mouse_scroll_wheel_up: '#409EFF',
    keyboard_input: '#67C23A',
    keyboard_clear: '#67C23A',
    keyboard_select_all: '#67C23A',
    keyboard_enter: '#67C23A',
    keyboard_combination_key: '#67C23A',
    flow_wait: '#E6A23C',
    flow_wait_element: '#E6A23C',
    flow_case_template: '#F56C6C',
    pip_switch_click: '#909399',
    pip_timeline_drag: '#909399',
    pip_slider_drag: '#909399',
  }
  return colorMap[props.data.step_type] || '#909399'
})

// 步骤内容摘要（给用户一眼看到关键信息）
const summary = computed(() => {
  const req = props.data.pc_request
  if (!req) return ''
  const t = props.data.step_type
  if (t === 'keyboard_input') return `输入: ${req.input_text || ''}`
  if (t === 'flow_wait') return `等待 ${req.wait_time ?? 1}s`
  if (t === 'flow_case_template') return `模板: ${req.case_template_name || ''}`
  if (t === 'keyboard_combination_key') return `组合键: ${(req.key_combination || []).join('+')}`
  if (req.image_name) return `素材: ${req.image_name}`
  return ''
})

const copyNode = (data) => {
  emit('copy-node', data)
}

const deletedNode = () => {
  emit('deleted-node')
}
</script>

<style lang="scss" scoped>
.pc-step-node {
  width: 100%;
  margin: 0;

  .step-card {
    min-height: 36px;

    :deep(.el-card__body) {
      padding: 6px 10px !important;
    }

    .step-header {
      display: flex;
      align-items: center;
      min-height: 28px;

      .step-header__right {
        margin-left: auto;
        display: flex;
        align-items: center;
        flex-shrink: 0;
      }
    }

    .step-summary {
      margin-top: 2px;
      padding-left: 4px;
      font-size: 12px;
      color: #909399;
    }
  }
}

:deep(.el-card) {
  border-radius: 6px;
  transition: border-color 0.2s;
}

.pc-mouse_left_click-border:hover,
.pc-mouse_right_click-border:hover,
.pc-mouse_double_click-border:hover,
.pc-mouse_hover-border:hover,
.pc-mouse_drag-border:hover,
.pc-mouse_scroll_wheel_down-border:hover,
.pc-mouse_scroll_wheel_up-border:hover { border-color: #409EFF; }

.pc-keyboard_input-border:hover,
.pc-keyboard_clear-border:hover,
.pc-keyboard_select_all-border:hover,
.pc-keyboard_enter-border:hover,
.pc-keyboard_combination_key-border:hover { border-color: #67C23A; }

.pc-flow_wait-border:hover,
.pc-flow_wait_element-border:hover { border-color: #E6A23C; }

.pc-flow_case_template-border:hover { border-color: #F56C6C; }

.pc-pip_switch_click-border:hover,
.pc-pip_timeline_drag-border:hover,
.pc-pip_slider_drag-border:hover { border-color: #909399; }
</style>

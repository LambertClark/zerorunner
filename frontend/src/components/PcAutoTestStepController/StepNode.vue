<template>
  <div class="pc-step-node" @click="handleHeaderClick">
    <el-card
        class="step-card w100"
        :class="[`pc-${step.step_type}-border`]"
        :style="{ borderColor: node.isCurrent ? getStepTypeInfo(step.step_type, 'color') : '' }"
    >
      <!-- 步骤头部 -->
      <div class="step-header">
        <!-- 步骤类型标签 -->
        <el-tag
            size="small"
            :color="getStepTypeInfo(step.step_type, 'color')"
            style="color: #fff; border: none; margin-right: 8px; flex-shrink: 0;"
        >
          {{ getStepTypeInfo(step.step_type, 'label') || step.step_type }}
        </el-tag>

        <!-- 展开/收起图标（仅可折叠类型） -->
        <span v-if="isCollapsibleType(step.step_type)" style="margin-right: 6px; color: #909399; font-size: 14px; cursor: pointer;">
          {{ isCollapsibleStep(step) ? '▼' : '▶' }}
        </span>

        <!-- 步骤名称 -->
        <div class="step-header__content" style="flex: 1; overflow: hidden;">
          <el-input
              v-if="step.edit"
              v-model="step.name"
              size="small"
              style="width: 200px;"
              @click.stop=""
              @blur="nameEditBlur"
          />
          <span v-else style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
            {{ step.name }}
          </span>
        </div>

        <!-- 操作区 -->
        <div class="step-header__right" @click.stop="">
          <el-tooltip content="启用/禁用" placement="top">
            <el-switch v-model="step.enable" inline-prompt size="small" style="margin-right: 6px"/>
          </el-tooltip>

          <el-button circle size="small" @click.stop="copyNode(step)">
            <el-icon><ele-DocumentCopy/></el-icon>
          </el-button>

          <el-button type="danger" circle size="small" @click.stop="deletedNode">
            <el-icon><ele-Delete/></el-icon>
          </el-button>
        </div>
      </div>

      <!-- 步骤详情区（根据 step_type 渲染不同控制器） -->
      <div class="step-details" v-if="isCollapsibleStep(step)" draggable="true" @dragstart.stop.prevent="">

        <template v-if="step.step_type === 'if'">
          <IfControllerHeader :data="step"/>
        </template>

        <template v-else-if="step.step_type === 'loop'">
          <LoopHeader :data="step"/>
          <LoopController :step="step"/>
        </template>

        <template v-else-if="step.step_type === 'flow_wait'">
          <WaitHeader :data="step"/>
        </template>

        <template v-else-if="step.step_type === 'flow_wait_element'">
          <WaitElementController v-model:data="step"/>
        </template>

        <template v-else-if="step.step_type === 'flow_case_template'">
          <CaseTemplateController v-model:data="step" @template-selected="handleTemplateSelected"/>
        </template>

        <template v-else-if="step.step_type.startsWith('mouse_') || step.step_type.startsWith('pip_')">
          <MouseController v-model:data="step"/>
        </template>

        <template v-else-if="step.step_type.startsWith('keyboard_')">
          <CombinationKeyController
              v-if="step.request && step.request.comparator === 'KEYBOARD_COMBINATION_KEY'"
              v-model:data="step"
          />
          <KeyboardController v-else v-model:data="step"/>
        </template>

      </div>
    </el-card>
  </div>
</template>

<script setup name="StepNode">
import { computed } from 'vue'
import IfControllerHeader from '/@/components/Z-StepController/ifController/IfControllerHeader.vue'
import LoopHeader from '/@/components/Z-StepController/loop/LoopHeader.vue'
import LoopController from '/@/components/Z-StepController/loop/LoopController.vue'
import MouseController from './MouseController/mouseController.vue'
import KeyboardController from './KeyboardController/keyboardController.vue'
import CombinationKeyController from './KeyboardController/combinationKeyController.vue'
import WaitHeader from '/@/components/Z-StepController/wait/WaitHeader.vue'
import WaitElementController from './FlowController/waitElementController.vue'
import CaseTemplateController from './FlowController/caseTemplateController.vue'
import { getStepTypeInfo } from '/@/utils/case'
import useVModel from '/@/utils/useVModel'

const emit = defineEmits(['copy-node', 'deleted-node'])

const props = defineProps({
  step: {
    type: Object,
    required: true,
  },
  node: {
    type: Object,
    required: true,
  },
  optType: {
    type: String,
    default: '',
  },
})

const step = useVModel(props, 'step', emit)

// 步骤名称失去焦点
const nameEditBlur = () => {
  step.value.edit = false
}

// 删除节点
const deletedNode = () => {
  emit('deleted-node')
}

// 切换详情展开状态
const toggleDetail = () => {
  step.value.showDetail = !step.value.showDetail
}

// 点击步骤头部
const handleHeaderClick = () => {
  if (isCollapsibleType(step.value.step_type)) {
    toggleDetail()
  }
}

// 模板被选中回调
const handleTemplateSelected = (templateInfo) => {
  if (templateInfo) {
    step.value.name = templateInfo.name || step.value.name
  }
}

// 复制节点
const copyNode = (data) => {
  emit('copy-node', data)
}

/**
 * 该步骤类型是否支持折叠展开
 * loop / pip_* / flow_wait_element 支持
 */
const isCollapsibleType = (stepType) => {
  if (!stepType) return false
  return stepType === 'loop' || stepType.startsWith('pip_') || stepType === 'flow_wait_element'
}

/**
 * 当前步骤是否处于展开状态
 * 鼠标基础点击默认不展开，仅复杂参数场景展开：
 *   - comparator === 'MOUSE_DRAG_ELEMENT_TO_ELEMENT'
 *   - 或 location_strategy === 'ANCHOR_OFFSET'
 */
const isCollapsibleStep = (stepData) => {
  if (!stepData) return false
  const t = stepData.step_type
  const req = stepData.request || {}

  // 鼠标基础点击：只有复杂参数时才展开
  if (t.startsWith('mouse_')) {
    if (req.comparator === 'MOUSE_DRAG_ELEMENT_TO_ELEMENT') return true
    if (req.location_strategy === 'ANCHOR_OFFSET') return true
    return false
  }

  // 可折叠类型：根据 showDetail 状态
  if (isCollapsibleType(t)) {
    return !!stepData.showDetail
  }

  // 其他类型（键盘、flow_wait、flow_case_template 等）始终显示详情
  if (t.startsWith('keyboard_') || t === 'flow_wait' || t === 'flow_case_template' || t === 'if') {
    return true
  }

  return !!stepData.showDetail
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

    .step-details {
      margin-top: 6px;
      padding-top: 6px;
      border-top: 1px solid #f0f0f0;
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
.pc-keyboard_combination_key-border:hover,
.pc-keyboard_single_key-border:hover { border-color: #67C23A; }

.pc-flow_wait-border:hover,
.pc-flow_wait_element-border:hover { border-color: #E6A23C; }

.pc-flow_case_template-border:hover { border-color: #F56C6C; }

.pc-pip_switch_click-border:hover,
.pc-pip_timeline_drag-border:hover,
.pc-pip_slider_drag-border:hover,
.pc-pip_drag-border:hover { border-color: #909399; }
</style>

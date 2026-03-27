<template>
  <div class="h100" id="pcStepController" style="overflow-y: auto">
    <el-backtop :right="200" :bottom="200" :visibility-height="10" target="#pcStepController"/>

    <div class="h100" style="overflow-y: auto">
      <el-tree
          ref="stepTreeRef"
          draggable
          highlight-current
          :allow-drop="allowDrop"
          node-key="id"
          :expand-on-click-node="false"
          :data="steps"
          @node-click="handleNodeClick"
          @node-drag-end="handleDragEnd"
      >
        <template #default="{ node }">
          <PcStepNode
              v-model:data="node.data"
              :node="node"
              @copy-node="copyNode"
              @deleted-node="deletedNode(node)"
              @node-click="handleNodeClick(node.data, node)"
          />
        </template>
      </el-tree>
    </div>

    <!-- 步骤详情抽屉 -->
    <el-drawer
        v-model="state.showDetail"
        size="520px"
        direction="rtl"
        :with-header="true"
        append-to-body
        destroy-on-close
        :close-on-click-modal="false"
    >
      <template #header>
        <strong>{{ getPcStepLabel(state.currentStep.step_type) }} - 步骤编辑</strong>
      </template>

      <div style="padding: 0 10px">
        <!-- 公共字段 -->
        <el-form label-width="90px" size="small">
          <el-form-item label="步骤名称">
            <el-input v-model="state.currentStep.name" placeholder="步骤名称" clearable/>
          </el-form-item>
          <el-form-item label="启用">
            <el-switch v-model="state.currentStep.enable"/>
          </el-form-item>
        </el-form>

        <el-divider/>

        <!-- 根据 step_type 渲染不同控制器 -->
        <MouseController
            v-if="isMouseStep(state.currentStep.step_type)"
            v-model:data="state.currentStep"
        />
        <KeyboardController
            v-else-if="isKeyboardStep(state.currentStep.step_type) && state.currentStep.step_type !== 'keyboard_combination_key'"
            v-model:data="state.currentStep"
        />
        <CombinationKeyController
            v-else-if="state.currentStep.step_type === 'keyboard_combination_key'"
            v-model:data="state.currentStep"
        />
        <WaitController
            v-else-if="state.currentStep.step_type === 'flow_wait'"
            v-model:data="state.currentStep"
        />
        <WaitElementController
            v-else-if="state.currentStep.step_type === 'flow_wait_element'"
            v-model:data="state.currentStep"
        />
        <CaseTemplateController
            v-else-if="state.currentStep.step_type === 'flow_case_template'"
            v-model:data="state.currentStep"
        />
      </div>
    </el-drawer>
  </div>
</template>

<script setup name="PcAutoTestStepController">
import { onMounted, reactive, ref } from 'vue'
import PcStepNode from './StepNode.vue'
import MouseController from './MouseController/mouseController.vue'
import KeyboardController from './KeyboardController/keyboardController.vue'
import CombinationKeyController from './KeyboardController/combinationKeyController.vue'
import WaitController from './FlowController/waitController.vue'
import WaitElementController from './FlowController/waitElementController.vue'
import CaseTemplateController from './FlowController/caseTemplateController.vue'
import {
  getPcStepLabel,
  isMouseStep,
  isKeyboardStep,
  createPcStepRequest,
} from '/@/hooks/pcAutoTest/useMouseData.js'

let _idCounter = 1

const emit = defineEmits(['update:steps'])

const props = defineProps({
  steps: {
    type: Array,
    default: () => [],
  },
  caseId: {
    type: [Number, String, null],
    default: null,
  },
})

const stepTreeRef = ref()

const state = reactive({
  showDetail: false,
  currentStep: {},
})

// 不允许内嵌（PC步骤是线性的）
const allowDrop = (draggingNode, dropNode, type) => {
  return type !== 'inner'
}

const handleDragEnd = () => {
  recomputeIndex(props.steps)
}

const recomputeIndex = (data) => {
  if (data) {
    data.forEach((item, idx) => {
      item.index = idx + 1
    })
  }
}

const handleNodeClick = (data) => {
  state.currentStep = data
  state.showDetail = true
}

// 生成本地唯一 id（后端保存后会替换）
const genTempId = () => `pc_tmp_${_idCounter++}`

// 根据 step_type 构造新步骤
const buildStepData = (step_type) => {
  return {
    id: genTempId(),
    name: getPcStepLabel(step_type),
    case_id: props.caseId,
    enable: true,
    index: 0,
    step_type,
    pc_request: createPcStepRequest(step_type),
    showDetail: false,
  }
}

// 对外暴露：新增步骤（由父组件的左侧面板调用）
const handleAddData = (step_type) => {
  const stepData = buildStepData(step_type)
  stepTreeRef.value.append(stepData, null)
  recomputeIndex(props.steps)
}

const deletedNode = (node) => {
  stepTreeRef.value.remove(node)
  recomputeIndex(props.steps)
}

const copyNode = (data) => {
  const copy = JSON.parse(JSON.stringify(data))
  copy.id = genTempId()
  props.steps.push(copy)
  recomputeIndex(props.steps)
}

onMounted(() => {})

defineExpose({
  handleAddData,
})
</script>

<style lang="scss" scoped>
:deep(.el-tree-node__content) {
  height: 100%;
  margin-top: 6px;
  vertical-align: center;
  display: flex;
  cursor: pointer;
  align-items: center;
}

:deep(.el-tree-node__label) {
  width: 100%;
}

.el-tree {
  padding: 10px;
  background: transparent !important;
}

:deep(.el-tree-node__expand-icon) {
  font-family: 'iconfont' !important;
  svg { display: none; }
  color: #1f1f1f;
  font-style: normal;
}

:deep(.el-tree-node__expand-icon.expanded) {
  -webkit-transform: rotate(0deg);
  transform: rotate(0deg);
}

:deep(.el-tree-node__expand-icon.expanded:before) {
  content: '\e61a';
  font-size: 18px;
}

:deep(.el-tree-node__expand-icon:before) {
  content: '\e61b';
  font-size: 18px;
}
</style>

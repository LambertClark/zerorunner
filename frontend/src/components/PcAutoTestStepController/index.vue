<template>
  <div class="h100" id="pcStepController" ref="scrollContainerRef" style="overflow-y: auto"
       @dragover.prevent="onDragOver">
    <el-backtop :right="200" :bottom="200" :visibility-height="10" target="#pcStepController"/>

    <div class="h100" style="overflow-y: auto">
      <el-tree
          ref="stepTreeRef"
          draggable
          highlight-current
          :allow-drop="allowDrop"
          node-key="id"
          :expand-on-click-node="false"
          :props="{ children: 'children_step' }"
          :data="steps"
          @node-click="nodeClick"
          @node-drag-start="handleDrop"
          @node-drag-end="handleDragEnd"
      >
        <template #default="{ node }">
          <StepNode
              v-model:step="node.data"
              :node="node"
              :opt-type="state.optType"
              @copy-node="copyNode"
              @deleted-node="deletedNode(node)"
          />
        </template>
      </el-tree>
    </div>
  </div>
</template>

<script setup name="pcStepController">
import { reactive, ref } from 'vue'
import StepNode from './StepNode.vue'
import useVModel from '/@/utils/useVModel'
import { useApiInfoApi } from '/@/api/useAutoApi/apiInfo'
import useMouseData from '/@/hooks/pcAutoTest/useMouseData.js'

const { operationTypeEnum } = useMouseData()

const emit = defineEmits(['update:steps', 'step-deleted'])

const props = defineProps({
  use_type: {
    type: String,
    default: () => 'case',
  },
  steps: {
    type: Array,
    default: () => [],
  },
  case_id: {
    type: [Number, String, null],
    default: () => null,
  },
})

const steps = useVModel(props, 'steps', emit)

const stepTreeRef = ref()
const scrollContainerRef = ref()
const isDragging = ref(false)
const dragClientY = ref(0)

const state = reactive({
  optType: '',
  optTypes: {},
  showApioInfo: false,
})

// 不允许内嵌（PC步骤是线性的）
const allowDrop = (draggingNode, dropNode, type) => {
  return type !== 'inner'
}

// 节点拖动开始
const handleDrop = (node, event) => {
  isDragging.value = true
}

// 节点拖动完成，重新计算顺序
const handleDragEnd = () => {
  isDragging.value = false
  stopAutoScroll()
  computeDataIndex(props.steps)
}

// 停止自动滚动
const stopAutoScroll = () => {
  isDragging.value = false
}

// 拖动时自动滚动容器
const autoScrollWhileDragging = () => {
  if (!isDragging.value || !scrollContainerRef.value) return
  const container = scrollContainerRef.value
  const { top, bottom, height } = container.getBoundingClientRect()
  const threshold = 60
  const speed = 8
  const y = dragClientY.value
  if (y - top < threshold) {
    container.scrollTop -= speed
  } else if (bottom - y < threshold) {
    container.scrollTop += speed
  }
}

// 拖动时更新鼠标位置
const onDragOver = (event) => {
  dragClientY.value = event.clientY
  autoScrollWhileDragging()
}

const nodeClick = (data, node) => {
  data.showDetail = !data.showDetail
}

// 重新计算 index
const computeDataIndex = (data, parentIndex = 0) => {
  if (data) {
    data.forEach((item, idx) => {
      item.index = idx + 1
      if (item.children_step) {
        computeDataIndex(item.children_step, parentIndex)
      }
    })
  }
}

// 对外暴露：新增步骤
const handleAddData = async (stepType) => {
  const stepData = getAddData(stepType)
  appendTreeDate(stepData)
}

// 添加到树
const appendTreeDate = (data) => {
  stepTreeRef.value?.append(data, null)
  computeDataIndex(props.steps)
}

// 获取步骤基础数据
const getStepData = () => {
  return {
    id: null,
    name: '',
    case_id: props.case_id,
    enable: true,
    index: 0,
    step_type: '',
    variables: [],
    setup_hooks: [],
    teardown_hooks: [],
    extracts: [],
    export: [],
    validators: [],
    request: null,
    showDetail: false,
    is_quotation: false,
    children_step: [],
  }
}

// 判断是否是需要特殊 request 的复合步骤类型
const isComplexStepType = (stepType) => {
  return stepType.startsWith('pip_') || stepType.startsWith('mouse_') ||
    stepType.startsWith('keyboard_') || stepType.startsWith('flow_')
}

// 根据 stepType 获取完整步骤数据
const getAddData = (stepType) => {
  const data = getStepData()
  data.step_type = stepType
  data.name = stepType + '_' + getRandomStr()

  if (stepType.startsWith('flow_')) {
    data.request = getFlowRequestData(stepType)
  } else if (stepType.startsWith('keyboard_')) {
    data.request = getKeyboardRequestData(stepType)
  } else if (stepType.startsWith('pip_')) {
    data.request = getPipRequestData(stepType)
  } else if (stepType.startsWith('mouse_')) {
    data.request = getMouseRequestData(stepType)
  }

  return data
}

// 流程控制 request 数据
const getFlowRequestData = (stepType) => {
  const comparator = operationTypeEnum[stepType] || ''
  if (stepType === 'flow_wait') {
    return { comparator, wait_time: 0 }
  }
  if (stepType === 'flow_wait_element') {
    return {
      comparator,
      image: '',
      waitElementType: '',
      picture_is_search: true,
      wait_time: 0,
      maskRegions: [],
    }
  }
  return { comparator }
}

// 键盘 request 数据
const getKeyboardRequestData = (stepType) => {
  return {
    comparator: operationTypeEnum[stepType] || '',
    keys: [],
    text: '',
  }
}

// PIP request 数据
const getPipRequestData = (stepType) => {
  const base = {
    comparator: operationTypeEnum[stepType] || '',
    image: '',
    referenceImage: '',
    location_strategy: 'PIP',
    picture_is_search: true,
    regionOffsetX: 0,
    regionOffsetY: 0,
    regionWidth: 0,
    regionHeight: 0,
    pipRegionX: 0,
    pipRegionY: 0,
    pipRegionWidth: 0,
    pipRegionHeight: 0,
  }
  if (['pip_drag', 'pip_slider_drag', 'pip_timeline_drag'].includes(stepType)) {
    Object.assign(base, {
      trackImage: '',
      trackRegionOffsetX: 0,
      trackRegionOffsetY: 0,
      trackRegionWidth: 0,
      trackRegionHeight: 0,
      targetPercentage: 50,
      isHorizontal: true,
    })
  }
  return base
}

// 鼠标 request 数据
const getMouseRequestData = (stepType) => {
  return {
    comparator: operationTypeEnum[stepType] || '',
    image: '',
    dragImage: '',
    picture_is_search: true,
    location_strategy: 'BASIC',
    referenceImage: '',
    regionOffsetX: 0,
    regionOffsetY: 0,
    regionWidth: 0,
    regionHeight: 0,
    maskRegions: [],
  }
}

// 添加 API 步骤（引用步骤用）
const addApiStep = async () => {
  state.showApioInfo = false
}

const getRandomStr = () => {
  return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1)
}

const deletedNode = (node) => {
  stepTreeRef.value.remove(node)
  computeDataIndex(props.steps)
  emit('step-deleted', node.data)
}

const copyNode = (data) => {
  const copy = JSON.parse(JSON.stringify(data))
  copy.id = null
  steps.value.push(copy)
  computeDataIndex(props.steps)
}

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

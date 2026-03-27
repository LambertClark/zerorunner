/**
 * PC 自动化步骤类型映射
 *
 * operationTypeEnum   : step_type（前端标识） -> 后端/执行端操作码
 * operationTypeToZh   : 操作码 -> 中文名称
 * pcStepGroups        : 按分组组织的步骤清单（用于左侧组件面板）
 */

// step_type -> 操作码
export const operationTypeEnum = {
  mouse_left_click: 'MOUSE_LEFT_CLICK',
  mouse_right_click: 'MOUSE_RIGHT_CLICK',
  mouse_double_click: 'MOUSE_DOUBLE_CLICK',
  mouse_hover: 'MOUSE_HOVER',
  mouse_drag: 'MOUSE_DRAG',
  mouse_scroll_wheel_down: 'MOUSE_SCROLL_WHEEL_DOWN',
  mouse_scroll_wheel_up: 'MOUSE_SCROLL_WHEEL_UP',
  keyboard_input: 'KEYBOARD_INPUT',
  keyboard_clear: 'KEYBOARD_CLEAR',
  keyboard_select_all: 'KEYBOARD_SELECT_ALL',
  keyboard_enter: 'KEYBOARD_ENTER',
  keyboard_combination_key: 'KEYBOARD_COMBINATION_KEY',
  flow_wait: 'FLOW_WAIT',
  flow_wait_element: 'FLOW_WAIT_ELEMENT',
  flow_case_template: 'FLOW_CASE_TEMPLATE',
  pip_switch_click: 'PIP_SWITCH_CLICK',
  pip_timeline_drag: 'PIP_TIMELINE_DRAG',
  pip_slider_drag: 'PIP_SLIDER_DRAG',
}

// 操作码 -> 中文名称
export const operationTypeToZh = {
  MOUSE_LEFT_CLICK: '左键点击',
  MOUSE_RIGHT_CLICK: '右键点击',
  MOUSE_DOUBLE_CLICK: '双击',
  MOUSE_HOVER: '鼠标悬停',
  MOUSE_DRAG: '鼠标拖拽',
  MOUSE_SCROLL_WHEEL_DOWN: '滚轮向下',
  MOUSE_SCROLL_WHEEL_UP: '滚轮向上',
  KEYBOARD_INPUT: '文本输入',
  KEYBOARD_CLEAR: '清除文本',
  KEYBOARD_SELECT_ALL: '全选',
  KEYBOARD_ENTER: '回车',
  KEYBOARD_COMBINATION_KEY: '组合键',
  FLOW_WAIT: '等待',
  FLOW_WAIT_ELEMENT: '元素追踪',
  FLOW_CASE_TEMPLATE: '引用模板',
  PIP_SWITCH_CLICK: 'PIP 开关点击',
  PIP_TIMELINE_DRAG: 'PIP 时间轴拖拽',
  PIP_SLIDER_DRAG: 'PIP 滑块拖拽',
}

/**
 * 按分组组织的步骤清单
 * 每个步骤包含：label（中文名）、step_type（前端key）、icon（iconfont class）
 */
export const pcStepGroups = [
  {
    groupLabel: '鼠标操作',
    color: '#409EFF',
    steps: [
      { label: '左键点击', step_type: 'mouse_left_click', icon: 'iconfont icon-mouse' },
      { label: '右键点击', step_type: 'mouse_right_click', icon: 'iconfont icon-mouse' },
      { label: '双击', step_type: 'mouse_double_click', icon: 'iconfont icon-mouse' },
      { label: '鼠标悬停', step_type: 'mouse_hover', icon: 'iconfont icon-mouse' },
      { label: '鼠标拖拽', step_type: 'mouse_drag', icon: 'iconfont icon-mouse' },
      { label: '滚轮向下', step_type: 'mouse_scroll_wheel_down', icon: 'iconfont icon-mouse' },
      { label: '滚轮向上', step_type: 'mouse_scroll_wheel_up', icon: 'iconfont icon-mouse' },
    ],
  },
  {
    groupLabel: '键盘操作',
    color: '#67C23A',
    steps: [
      { label: '文本输入', step_type: 'keyboard_input', icon: 'iconfont icon-keyboard' },
      { label: '清除文本', step_type: 'keyboard_clear', icon: 'iconfont icon-keyboard' },
      { label: '全选', step_type: 'keyboard_select_all', icon: 'iconfont icon-keyboard' },
      { label: '回车', step_type: 'keyboard_enter', icon: 'iconfont icon-keyboard' },
      { label: '组合键', step_type: 'keyboard_combination_key', icon: 'iconfont icon-keyboard' },
    ],
  },
  {
    groupLabel: '流程控制',
    color: '#E6A23C',
    steps: [
      { label: '等待', step_type: 'flow_wait', icon: 'iconfont icon-time' },
      { label: '元素追踪', step_type: 'flow_wait_element', icon: 'iconfont icon-time' },
      { label: '引用模板', step_type: 'flow_case_template', icon: 'iconfont icon-a-case-o1' },
    ],
  },
  {
    groupLabel: 'PIP 操作',
    color: '#F56C6C',
    steps: [
      { label: 'PIP 开关点击', step_type: 'pip_switch_click', icon: 'iconfont icon-mouse' },
      { label: 'PIP 时间轴拖拽', step_type: 'pip_timeline_drag', icon: 'iconfont icon-mouse' },
      { label: 'PIP 滑块拖拽', step_type: 'pip_slider_drag', icon: 'iconfont icon-mouse' },
    ],
  },
]

/**
 * 根据 step_type 获取中文名称
 */
export function getPcStepLabel(step_type) {
  const code = operationTypeEnum[step_type]
  return code ? (operationTypeToZh[code] || step_type) : step_type
}

/**
 * 根据 step_type 判断所属分组（返回 groupLabel）
 */
export function getPcStepGroup(step_type) {
  for (const group of pcStepGroups) {
    if (group.steps.some((s) => s.step_type === step_type)) {
      return group.groupLabel
    }
  }
  return ''
}

/**
 * 鼠标类步骤（需要图片素材 + 坐标）
 */
export const mouseStepTypes = [
  'mouse_left_click',
  'mouse_right_click',
  'mouse_double_click',
  'mouse_hover',
  'mouse_drag',
  'mouse_scroll_wheel_down',
  'mouse_scroll_wheel_up',
  'pip_switch_click',
  'pip_timeline_drag',
  'pip_slider_drag',
]

/**
 * 键盘类步骤
 */
export const keyboardStepTypes = [
  'keyboard_input',
  'keyboard_clear',
  'keyboard_select_all',
  'keyboard_enter',
  'keyboard_combination_key',
]

/**
 * 是否是鼠标类步骤
 */
export function isMouseStep(step_type) {
  return mouseStepTypes.includes(step_type)
}

/**
 * 是否是键盘类步骤
 */
export function isKeyboardStep(step_type) {
  return keyboardStepTypes.includes(step_type)
}

/**
 * 生成 PC 步骤默认 request 数据
 */
export function createPcStepRequest(step_type) {
  const base = {
    operation_type: operationTypeEnum[step_type] || '',
  }

  if (isMouseStep(step_type)) {
    return {
      ...base,
      image_id: null,
      image_name: '',
      image_url: '',
      threshold: 0.8,
      timeout: 10,
      // mouse_drag 额外字段
      to_image_id: null,
      to_image_name: '',
      to_image_url: '',
      // scroll
      scroll_times: 3,
    }
  }

  if (step_type === 'keyboard_input') {
    return { ...base, input_text: '' }
  }

  if (step_type === 'keyboard_combination_key') {
    return { ...base, key_combination: [] }
  }

  if (['keyboard_clear', 'keyboard_select_all', 'keyboard_enter'].includes(step_type)) {
    return { ...base }
  }

  if (step_type === 'flow_wait') {
    return { ...base, wait_time: 1 }
  }

  if (step_type === 'flow_wait_element') {
    return {
      ...base,
      image_id: null,
      image_name: '',
      image_url: '',
      threshold: 0.8,
      timeout: 30,
    }
  }

  if (step_type === 'flow_case_template') {
    return { ...base, case_template_id: null, case_template_name: '' }
  }

  return { ...base }
}

// 流程控制组件
export const flowComponents = [
  { label: '等待', step_type: 'flow_wait' },
  { label: '元素追踪', step_type: 'flow_wait_element' },
  // {label: 'API', step_type: 'api'},
  // {label: 'IF', step_type: 'if'},
  // {label: 'Loop', step_type: 'loop'},
  // {label: '脚本', step_type: 'script'},
  // {label: 'SQL', step_type: 'sql'},
]

// 模板用例额外包含模板导入
export const templateFlowComponents = [
  ...flowComponents,
  { label: '模板导入', step_type: 'flow_case_template' },
]

// 鼠标操作组件
export const mouseComponents = [
  { label: '左键点击', step_type: 'mouse_left_click' },
  { label: '右键点击', step_type: 'mouse_right_click' },
  { label: '左键双击', step_type: 'mouse_double_click' },
  { label: '移入', step_type: 'mouse_hover' },
  { label: '拖拽', step_type: 'mouse_drag' },
  { label: '向下滚动', step_type: 'mouse_scroll_wheel_down' },
  { label: '向上滚动', step_type: 'mouse_scroll_wheel_up' },
  { label: '图中图-点击', step_type: 'pip_switch_click' },
  { label: '图中图-拖拽', step_type: 'pip_slider_drag' },
]

// 键盘操作组件
export const keyboardComponents = [
  { label: '文本输入', step_type: 'keyboard_input' },
  { label: '快捷键', step_type: 'keyboard_combination_key' },
  { label: '清空', step_type: 'keyboard_clear' },
  { label: '全选', step_type: 'keyboard_select_all' },
  { label: '回车', step_type: 'keyboard_enter' },
]

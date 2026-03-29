<template>
  <div class="combination-key-controller">
    <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
      <!-- 已录入的键 -->
      <el-tag
          v-for="(key, idx) in data.request.keys"
          :key="idx"
          closable
          @close="removeKey(idx)"
      >{{ key }}</el-tag>

      <!-- 录制按钮 -->
      <el-button
          size="small"
          :type="isListening ? 'danger' : 'primary'"
          @click="isListening ? stopListening() : startListening()"
      >
        {{ capturePrompt }}
      </el-button>

      <!-- 清空 -->
      <el-button
          v-if="data.request.keys && data.request.keys.length"
          size="small"
          @click="clearAll"
      >清空</el-button>

      <!-- 组合键预览 -->
      <span
          v-if="data.request.keys && data.request.keys.length"
          style="font-size: 13px; color: #409eff; margin-left: 4px;"
      >
        {{ data.request.keys.join(' + ') }}
      </span>
    </div>
  </div>
</template>

<script setup name="keyboardController">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import useVModel from '/@/utils/useVModel'
import useMouseData from '/@/hooks/pcAutoTest/useMouseData.js'

const props = defineProps({
  data: { type: Object, required: true },
})
const emit = defineEmits(['update:data'])
const data = useVModel(props, 'data', emit)

const { operationTypeEnum } = useMouseData()

const isListening = ref(false)
const isMac = ref(navigator.platform.toUpperCase().includes('MAC'))

const keyMap = {
  Control: isMac.value ? '⌃' : 'CTRL',
  Alt:     isMac.value ? '⌥' : 'ALT',
  Shift:   isMac.value ? '⇧' : 'SHIFT',
  Meta:    isMac.value ? '⌘' : 'WIN',
}

const specialKeys = new Set([
  ' ', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight',
  'Enter', 'Backspace', 'Escape', 'Tab', 'CapsLock', 'Shift',
  'Delete', 'Home', 'End', 'PageUp', 'PageDown', 'Insert',
])

const specialKeyNames = {
  ' ':          'Space',
  'ArrowUp':    '↑',
  'ArrowDown':  '↓',
  'ArrowLeft':  '←',
  'ArrowRight': '→',
  'Enter':      'Enter',
  'Backspace':  'Backspace',
  'Escape':     'Escape',
  'Tab':        'Tab',
  'CapsLock':   'CapsLock',
  'Delete':     'Delete',
  'Home':       'Home',
  'End':        'End',
  'PageUp':     'PageUp',
  'PageDown':   'PageDown',
  'Insert':     'Insert',
}

function keyDisplay(keyValue) {
  if (keyMap[keyValue]) return keyMap[keyValue]
  if (specialKeyNames[keyValue]) return specialKeyNames[keyValue]
  if (specialKeys.has(keyValue)) return keyValue
  return keyValue.length === 1 ? keyValue.toUpperCase() : keyValue
}

function logStep(msg) {
  console.log('[CombinationKey]', msg)
}

function startListening() {
  if (!data.value.request.keys) {
    data.value.request.keys = []
  }
  isListening.value = true
  logStep('开始录制按键')
}

function stopListening() {
  isListening.value = false
  logStep('停止录制按键')
}

function handleKeyDown(event) {
  if (!isListening.value) return
  if (event.repeat) return
  event.preventDefault()

  // ESC 停止录制
  if (event.key === 'Escape') {
    stopListening()
    return
  }

  const keys = data.value.request.keys || []
  if (keys.length >= 3) return

  const display = keyDisplay(event.key)
  if (!keys.includes(display)) {
    data.value.request.keys = [...keys, display]
    logStep(`录入按键: ${display}`)
  }

  if ((data.value.request.keys || []).length >= 3) {
    stopListening()
  }
}

function removeKey(idx) {
  const keys = [...(data.value.request.keys || [])]
  keys.splice(idx, 1)
  data.value.request.keys = keys
}

function clearAll() {
  data.value.request.keys = []
  isListening.value = false
}

const capturePrompt = computed(() => {
  const keys = data.value.request.keys || []
  if (isListening.value && keys.length < 3) return `录入${keys.length}个按键...`
  if (keys.length >= 3) return '已达最大记录数（3键）'
  return '录入快捷键'
})

onMounted(() => window.addEventListener('keydown', handleKeyDown))
onBeforeUnmount(() => window.removeEventListener('keydown', handleKeyDown))
</script>

<style lang="scss" scoped>
.combination-key-controller {
  padding: 4px 0;
}
</style>

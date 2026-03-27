<template>
  <div class="combination-key-controller">
    <el-form label-width="90px" size="small">
      <el-form-item label="组合键">
        <div style="width: 100%">
          <el-tag
              v-for="(key, idx) in data.pc_request.key_combination"
              :key="idx"
              closable
              style="margin: 0 4px 4px 0"
              @close="removeKey(idx)"
          >
            {{ key }}
          </el-tag>
          <el-select
              v-model="state.inputKey"
              placeholder="添加按键"
              filterable
              style="width: 140px; margin-top: 4px"
              @change="addKey"
          >
            <el-option v-for="k in commonKeys" :key="k" :label="k" :value="k"/>
          </el-select>
        </div>
      </el-form-item>

      <el-form-item label="预览">
        <el-text>{{ (data.pc_request.key_combination || []).join(' + ') || '-' }}</el-text>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup name="CombinationKeyController">
import { reactive } from 'vue'

const props = defineProps({
  data: {
    type: Object,
    default: () => ({}),
  },
})

const state = reactive({
  inputKey: '',
})

const commonKeys = [
  'ctrl', 'alt', 'shift', 'win',
  'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
  'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
  'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
  'enter', 'esc', 'tab', 'backspace', 'delete', 'space',
  'up', 'down', 'left', 'right',
]

const addKey = (key) => {
  if (!key) return
  if (!props.data.pc_request.key_combination) {
    props.data.pc_request.key_combination = []
  }
  if (!props.data.pc_request.key_combination.includes(key)) {
    props.data.pc_request.key_combination.push(key)
  }
  state.inputKey = ''
}

const removeKey = (idx) => {
  props.data.pc_request.key_combination.splice(idx, 1)
}
</script>

<style lang="scss" scoped>
.combination-key-controller {
  padding: 0 4px;
}
</style>

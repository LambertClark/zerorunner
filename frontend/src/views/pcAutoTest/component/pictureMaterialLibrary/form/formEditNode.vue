<template>
  <el-dialog
    v-model="visible"
    :title="dialogTitle"
    width="400px"
    append-to-body
    destroy-on-close
    :close-on-click-modal="false"
  >
    <el-form ref="formRef" :model="state.form" label-width="80px" size="small">
      <el-form-item label="节点名称" required>
        <el-input v-model="state.form.name" placeholder="请输入节点名称" clearable @keyup.enter="handleSubmit" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="handleCancel">取消</el-button>
      <el-button type="primary" :loading="loading" @click="handleSubmit">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive } from 'vue'

const emit = defineEmits(['handleEditNodeSubmit'])

const visible = ref(false)
const loading = ref(false)
const formRef = ref()
const dialogTitle = '编辑节点'

const state = reactive({
  form: {
    id: null,
    name: '',
    currentNode: null,
  },
})

function openDialog(nodeData) {
  state.form.id = nodeData?.id
  state.form.name = nodeData?.label || nodeData?.name || ''
  state.form.currentNode = nodeData
  visible.value = true
}

function fullReset() {
  state.form.id = null
  state.form.name = ''
  state.form.currentNode = null
  visible.value = false
}

function handleSubmit() {
  if (!state.form.name?.trim()) return
  emit('handleEditNodeSubmit', { id: state.form.id, name: state.form.name })
  fullReset()
}

function handleReset() {
  fullReset()
}

function handleCancel() {
  fullReset()
}

defineExpose({ openDialog })
</script>

<template>
  <el-dialog
    v-model="visible"
    :title="dialogTitle"
    width="400px"
    append-to-body
    destroy-on-close
    :close-on-click-modal="false"
  >
    <el-form ref="formRef" :model="state.form" :rules="state.rules" label-width="80px" size="small">
      <el-form-item label="节点名称" prop="name">
        <el-input v-model="state.form.name" placeholder="请输入节点名称" clearable @keyup.enter="handleSubmit" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="handleReset">取消</el-button>
      <el-button type="primary" @click="handleSubmit">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'

const emit = defineEmits(['handleAddNodeSubmit'])

const visible = ref(false)
const formRef = ref()

const state = reactive({
  form: {
    currentNode: null,
    name: '',
  },
  rules: {
    name: [{ required: true, message: '请输入节点名称', trigger: 'blur' }],
  },
})

const dialogTitle = computed(() => (state.form.currentNode ? '添加子节点' : '添加根节点'))

function openDialog(parentNode = null) {
  state.form.currentNode = parentNode
  state.form.name = ''
  visible.value = true
}

function fullReset() {
  state.form.currentNode = null
  state.form.name = ''
  visible.value = false
}

function handleSubmit() {
  formRef.value?.validate((valid) => {
    if (!valid) return
    emit('handleAddNodeSubmit', { name: state.form.name, parentNode: state.form.currentNode })
    fullReset()
  })
}

function handleReset() {
  fullReset()
}

defineExpose({ openDialog })
</script>

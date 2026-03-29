<template>
  <el-dialog
      v-model="visible"
      title="重命名节点"
      width="400px"
      append-to-body
      destroy-on-close
  >
    <el-form :model="form" label-width="80px" size="small">
      <el-form-item label="节点名称" required>
        <el-input v-model="form.name" placeholder="请输入新名称" clearable @keyup.enter="submit"/>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="visible = false">取消</el-button>
      <el-button type="primary" @click="submit">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup name="formEditNode">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const emit = defineEmits(['submit'])

const visible = ref(false)
const nodeData = ref(null)
const form = reactive({ name: '' })

function open(data) {
  nodeData.value = data
  form.name = data?.name || ''
  visible.value = true
}

function submit() {
  if (!form.name.trim()) {
    ElMessage.warning('节点名称不能为空')
    return
  }
  emit('submit', {
    id: nodeData.value?.id,
    name: form.name.trim(),
  })
  visible.value = false
}

defineExpose({ open })
</script>

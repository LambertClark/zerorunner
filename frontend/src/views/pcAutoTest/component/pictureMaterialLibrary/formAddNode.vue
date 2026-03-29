<template>
  <el-dialog
      v-model="visible"
      :title="parentData ? '添加子节点' : '添加根节点'"
      width="400px"
      append-to-body
      destroy-on-close
  >
    <el-form :model="form" label-width="80px" size="small">
      <el-form-item label="节点名称" required>
        <el-input v-model="form.name" placeholder="请输入节点名称" clearable @keyup.enter="submit"/>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="visible = false">取消</el-button>
      <el-button type="primary" @click="submit">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup name="FormAddNode">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const emit = defineEmits(['submit'])

const visible = ref(false)
const parentData = ref(null)
const form = reactive({ name: '' })

function open(parent = null) {
  parentData.value = parent
  form.name = ''
  visible.value = true
}

function submit() {
  if (!form.name.trim()) {
    ElMessage.warning('节点名称不能为空')
    return
  }
  emit('submit', {
    name: form.name.trim(),
    parent_id: parentData.value?.id ?? null,
  })
  visible.value = false
}

defineExpose({ open })
</script>

<template>
  <el-dialog
    v-model="visible"
    title="添加素材"
    width="480px"
    append-to-body
    destroy-on-close
    :close-on-click-modal="false"
  >
    <el-form ref="formRef" :model="state.form" label-width="80px" size="small">
      <el-form-item label="素材名称" required>
        <el-input v-model="state.form.name" placeholder="请输入素材名称" clearable />
      </el-form-item>
      <el-form-item label="粘贴图片">
        <div class="paste-area" tabindex="0" @paste="handlePaste">
          <img v-if="previewBase64" :src="previewBase64" style="max-width: 100%; max-height: 180px;" />
          <span v-else style="color: #909399; font-size: 13px;">点击此处后按 Ctrl+V 粘贴图片</span>
        </div>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="handleReset">取消</el-button>
      <el-button type="primary" :loading="saving" @click="handleSubmit">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { usePcFileManagerApi } from '/@/api/usePcAutoApi/pcFileManager.js'
import { usePcPictureApi } from '/@/api/usePcAutoApi/pcPicture.js'

const emit = defineEmits(['handleAddPictureSubmit'])

const visible = ref(false)
const saving = ref(false)
const previewBase64 = ref('')
const formRef = ref()

const state = reactive({
  form: {
    tree_id: null,
    name: '',
    file: null,
    image_url: '',
  },
})

function openDialog(imageData) {
  state.form.tree_id = imageData.id
  state.form.name = ''
  state.form.file = null
  state.form.image_url = ''
  previewBase64.value = ''
  visible.value = true
}

function handlePaste(event) {
  const items = (event.clipboardData || event.originalEvent?.clipboardData)?.items
  if (!items) return
  for (const item of items) {
    if (item.type.startsWith('image/')) {
      const file = item.getAsFile()
      const reader = new FileReader()
      reader.onload = (e) => {
        previewBase64.value = e.target.result
      }
      reader.readAsDataURL(file)
      state.form.file = file
      break
    }
  }
}

async function handleSubmit() {
  if (!state.form.name?.trim()) {
    ElMessage.warning('请输入素材名称')
    return
  }
  if (!state.form.file) {
    ElMessage.warning('请先粘贴图片')
    return
  }
  saving.value = true
  try {
    const formDataTemp = new FormData()
    formDataTemp.append('file', state.form.file)
    const res = await usePcFileManagerApi().uploadPhoto(formDataTemp)
    state.form.image_url = res.data.path
    await usePcPictureApi().saveOrUpdatePicture({
      tree_id: state.form.tree_id,
      image_url: state.form.image_url,
      name: state.form.name,
    })
    ElMessage.success('添加成功')
    emit('handleAddPictureSubmit')
    fullReset()
  } catch {
    ElMessage.error('添加失败')
  } finally {
    saving.value = false
  }
}

function handleReset() {
  fullReset()
}

function fullReset() {
  state.form.tree_id = null
  state.form.name = ''
  state.form.file = null
  state.form.image_url = ''
  previewBase64.value = ''
  visible.value = false
}

defineExpose({ openDialog })
</script>

<style scoped>
.paste-area {
  width: 100%;
  min-height: 80px;
  border: 1px dashed #dcdfe6;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
  cursor: pointer;
  outline: none;
}

.paste-area:focus {
  border-color: #409eff;
}
</style>

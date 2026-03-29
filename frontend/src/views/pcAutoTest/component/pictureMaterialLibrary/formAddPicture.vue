<template>
  <el-dialog
      v-model="visible"
      title="添加素材"
      width="480px"
      append-to-body
      destroy-on-close
      :close-on-click-modal="false"
  >
    <el-form :model="form" label-width="80px" size="small">
      <el-form-item label="素材名称" required>
        <el-input v-model="form.name" placeholder="请输入素材名称" clearable/>
      </el-form-item>
      <el-form-item label="所属节点">
        <el-input :value="nodeData ? nodeData.name : ''" disabled/>
      </el-form-item>
      <el-form-item label="素材图片" required>
        <el-upload
            action="#"
            :auto-upload="false"
            :on-change="handleFileChange"
            :show-file-list="true"
            accept="image/*"
        >
          <el-button type="primary">选择图片</el-button>
        </el-upload>
      </el-form-item>
      <el-form-item label="备注">
        <el-input v-model="form.remarks" placeholder="备注"/>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="visible = false">取消</el-button>
      <el-button type="primary" :loading="saving" @click="submit">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup name="FormAddPicture">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { usePcFileManagerApi } from '/@/api/usePcAutoApi/pcFileManager.js'
import { usePcPictureApi } from '/@/api/usePcAutoApi/pcPicture.js'

const emit = defineEmits(['saved'])

const visible = ref(false)
const saving = ref(false)
const nodeData = ref(null)
const pendingFile = ref(null)
const form = reactive({ name: '', remarks: '' })

function open(node) {
  nodeData.value = node
  form.name = ''
  form.remarks = ''
  pendingFile.value = null
  visible.value = true
}

function handleFileChange(file) {
  pendingFile.value = file.raw
}

async function submit() {
  if (!form.name.trim()) {
    ElMessage.warning('素材名称不能为空')
    return
  }
  if (!pendingFile.value) {
    ElMessage.warning('请选择图片文件')
    return
  }
  saving.value = true
  try {
    const formData = new FormData()
    formData.append('file', pendingFile.value)
    const uploadRes = await usePcFileManagerApi().uploadPhoto(formData)
    const filePath = uploadRes.data?.file_path || uploadRes.data?.url || ''

    await usePcPictureApi().saveOrUpdatePicture({
      name: form.name.trim(),
      tree_id: nodeData.value?.id ?? null,
      file_path: filePath,
      remarks: form.remarks,
    })
    ElMessage.success('添加成功')
    emit('saved')
    visible.value = false
  } catch {
    ElMessage.error('添加失败')
  } finally {
    saving.value = false
  }
}

defineExpose({ open })
</script>

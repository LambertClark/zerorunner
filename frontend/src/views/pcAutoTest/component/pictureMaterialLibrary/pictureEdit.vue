<template>
  <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑素材' : '新增素材'"
      width="560px"
      append-to-body
      destroy-on-close
      :close-on-click-modal="false"
  >
    <el-form
        ref="formRef"
        :model="state.form"
        :rules="state.rules"
        label-width="90px"
        size="small"
    >
      <el-form-item label="素材名称" prop="name">
        <el-input v-model="state.form.name" placeholder="请输入素材名称" clearable/>
      </el-form-item>

      <el-form-item label="所属树节点" prop="tree_id">
        <el-select v-model="state.form.tree_id" placeholder="选择素材树节点" filterable style="width: 100%">
          <el-option
              v-for="node in state.treeList"
              :key="node.id"
              :label="node.name"
              :value="node.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="素材文件" prop="file">
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

      <el-form-item label="当前图片" v-if="state.form.file_path">
        <el-image
            :src="picUrl"
            fit="contain"
            style="width: 120px; height: 80px; border: 1px solid #ddd; border-radius: 4px;"
            :preview-src-list="[picUrl]"
            preview-teleported
        />
      </el-form-item>

      <el-form-item label="备注">
        <el-input v-model="state.form.remarks" placeholder="备注"/>
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" :loading="state.saving" @click="save">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup name="PictureEdit">
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { usePcPictureApi } from '/@/api/usePcAutoApi/pcPicture.js'
import { usePcFileManagerApi } from '/@/api/usePcAutoApi/pcFileManager.js'
import { getBaseApiUrl } from '/@/utils/config'

const props = defineProps({
  visible: { type: Boolean, default: false },
  picture: { type: Object, default: null },
})
const emit = defineEmits(['update:visible', 'saved'])

const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => emit('update:visible', val),
})

const isEdit = computed(() => !!props.picture?.id)

const formRef = ref()
const pictureApi = usePcPictureApi()
const fileApi = usePcFileManagerApi()

const state = reactive({
  form: {
    id: null,
    name: '',
    tree_id: null,
    file_path: '',
    remarks: '',
  },
  rules: {
    name: [{ required: true, message: '请输入素材名称', trigger: 'blur' }],
  },
  treeList: [],
  pendingFile: null,
  saving: false,
})

const picUrl = computed(() => {
  const url = state.form.file_path
  if (!url) return ''
  return url.startsWith('http') ? url : `${getBaseApiUrl()}/${url}`
})

const fetchTree = () => {
  pictureApi.getTreeList({}).then((res) => {
    // 将树结构展平为列表
    state.treeList = flattenTree(res.data || [])
  })
}

const flattenTree = (nodes, result = []) => {
  nodes.forEach((node) => {
    result.push(node)
    if (node.children?.length) flattenTree(node.children, result)
  })
  return result
}

const handleFileChange = (file) => {
  state.pendingFile = file.raw
}

const save = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  state.saving = true
  try {
    // 如有新上传的文件，先上传
    if (state.pendingFile) {
      const formData = new FormData()
      formData.append('file', state.pendingFile)
      const uploadRes = await fileApi.upload(formData)
      state.form.file_path = uploadRes.data?.file_path || uploadRes.data?.url || ''
    }
    await pictureApi.saveOrUpdate(state.form)
    ElMessage.success('保存成功')
    emit('saved')
    dialogVisible.value = false
  } finally {
    state.saving = false
  }
}

onMounted(() => {
  fetchTree()
  if (props.picture) {
    state.form = { ...props.picture }
  }
})
</script>

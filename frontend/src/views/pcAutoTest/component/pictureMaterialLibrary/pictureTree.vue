<template>
  <div class="picture-tree">
    <div class="tree-toolbar">
      <el-button type="primary" size="small" @click="openAddNode(null)">新增根节点</el-button>
    </div>

    <el-tree
        ref="treeRef"
        :data="state.treeData"
        :props="{ label: 'name', children: 'children' }"
        node-key="id"
        highlight-current
        default-expand-all
        @node-click="handleNodeClick"
    >
      <template #default="{ node, data }">
        <div class="tree-node" style="display: flex; align-items: center; width: 100%; justify-content: space-between;">
          <span>{{ data.name }}</span>
          <span @click.stop style="flex-shrink: 0;">
            <el-button type="primary" link size="small" @click="openAddNode(data)">+子</el-button>
            <el-button type="warning" link size="small" @click="openEditNode(data)">改</el-button>
            <el-button type="danger" link size="small" @click="deleteNode(data)">删</el-button>
          </span>
        </div>
      </template>
    </el-tree>

    <!-- 新增/编辑节点弹窗 -->
    <el-dialog
        v-model="state.showNodeDialog"
        :title="state.nodeForm.id ? '编辑节点' : '新增节点'"
        width="400px"
        append-to-body
        destroy-on-close
    >
      <el-form :model="state.nodeForm" label-width="80px" size="small">
        <el-form-item label="节点名称" required>
          <el-input v-model="state.nodeForm.name" placeholder="请输入节点名称" clearable/>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="state.showNodeDialog = false">取消</el-button>
        <el-button type="primary" @click="saveNode">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="PictureTree">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { usePcPictureApi } from '/@/api/usePcAutoApi/pcPicture.js'

const emit = defineEmits(['node-click'])
const treeRef = ref()
const pictureApi = usePcPictureApi()

const state = reactive({
  treeData: [],
  showNodeDialog: false,
  nodeForm: {
    id: null,
    name: '',
    parent_id: null,
  },
})

const fetchTree = () => {
  pictureApi.getTreeList({}).then((res) => {
    state.treeData = res.data || []
  })
}

const handleNodeClick = (data) => {
  emit('node-click', data)
}

const openAddNode = (parentNode) => {
  state.nodeForm = { id: null, name: '', parent_id: parentNode?.id ?? null }
  state.showNodeDialog = true
}

const openEditNode = (data) => {
  state.nodeForm = { id: data.id, name: data.name, parent_id: data.parent_id ?? null }
  state.showNodeDialog = true
}

const saveNode = () => {
  if (!state.nodeForm.name) {
    ElMessage.warning('节点名称不能为空')
    return
  }
  pictureApi.saveOrUpdateTree(state.nodeForm).then(() => {
    ElMessage.success('保存成功')
    state.showNodeDialog = false
    fetchTree()
  })
}

const deleteNode = (data) => {
  ElMessageBox.confirm('删除该节点会同时删除其下所有素材，是否继续?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    pictureApi.deletedTree({ id: data.id }).then(() => {
      ElMessage.success('删除成功')
      fetchTree()
    })
  })
}

onMounted(() => {
  fetchTree()
})

defineExpose({ fetchTree })
</script>

<style lang="scss" scoped>
.picture-tree {
  height: 100%;

  .tree-toolbar {
    padding: 8px 0;
  }
}
</style>

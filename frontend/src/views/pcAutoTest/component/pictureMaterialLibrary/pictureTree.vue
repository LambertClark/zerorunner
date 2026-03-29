<template>
  <div class="picture-tree">
    <!-- 搜索框 -->
    <el-input
        v-model="filterText"
        placeholder="节点名称搜索"
        clearable
        size="small"
        style="margin-bottom: 8px;"
    />

    <!-- 添加根节点 -->
    <el-button type="primary" size="small" style="margin-bottom: 8px; width: 100%;" @click="appendRootNode">
      添加根节点
    </el-button>

    <!-- 树 -->
    <el-tree
        ref="treeRef"
        :data="dataSource"
        :props="{ label: 'name', children: 'children' }"
        node-key="id"
        highlight-current
        :default-expanded-keys="expandedKeys"
        :filter-node-method="filterNode"
        @node-expand="handleNodeExpand"
        @node-collapse="handleNodeCollapse"
        @node-click="handleNodeClick"
    >
      <template #default="{ node, data }">
        <div class="tree-node-row">
          <span class="tree-node-label">{{ data.name }}</span>
          <span class="tree-node-actions" @click.stop>
            <el-button type="primary" link size="small" @click="openPictureDialog(data)">素材</el-button>
            <el-button type="success" link size="small" @click="append(data)">+子</el-button>
            <el-button type="warning" link size="small" @click="openReNodeNameDialog(data)">改名</el-button>
            <el-button type="danger" link size="small" @click="remove(data)">删</el-button>
          </span>
        </div>
      </template>
    </el-tree>

    <!-- 子表单组件 -->
    <FormAddNode ref="addNodeForm" @handleAddNodeSubmit="appendAndSubmit"/>
    <formEditNode ref="editNodeForm" @handleEditNodeSubmit="handleDialogSubmit"/>
    <FormAddPicture ref="addPictureForm" @handleAddPictureSubmit="onPictureSaved"/>
  </div>
</template>

<script setup name="pictureTree">
import { ref, watch, nextTick, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { usePcPictureApi } from '/@/api/usePcAutoApi/pcPicture.js'
import emitter from '/@/utils/mitt.js'
import FormAddNode from './form/formAddNode.vue'
import formEditNode from './form/formEditNode.vue'
import FormAddPicture from './form/formAddPicture.vue'

const emit = defineEmits(['node-click'])

const treeRef = ref()
const addPictureForm = ref()
const addNodeForm = ref()
const editNodeForm = ref()

const dataSource = ref([])
const expandedKeys = ref([])
const currentNode = ref(null)
const filterText = ref('')

// 过滤方法
function filterNode(value, data) {
  if (!value) return true
  return data.name?.includes(value)
}

watch(filterText, (val) => {
  treeRef.value?.filter(val)
})

// 获取全部树
function getAllTree() {
  usePcPictureApi().getTree().then((res) => {
    dataSource.value = res.data || []
  })
}

// 按树节点ID查询图片，通过 emitter 推给右侧
function pictureByTreeId() {
  if (!currentNode.value) return
  usePcPictureApi().pictureByTreeId({ tree_id: currentNode.value.id }).then((res) => {
    const imageList = res.data || []
    const pictureEdit = { imageList, currentNode: currentNode.value }
    emitter.emit('picture-edit', pictureEdit)
  })
}

// 节点点击
function handleNodeClick(data) {
  currentNode.value = data
  emit('node-click', data)
  pictureByTreeId()
}

// 展开 / 折叠记录
function handleNodeExpand(data) {
  if (!expandedKeys.value.includes(data.id)) {
    expandedKeys.value.push(data.id)
  }
}

function handleNodeCollapse(data) {
  expandedKeys.value = expandedKeys.value.filter((k) => k !== data.id)
}

// 局部更新树节点名称
function updateNodeInTree(nodeData) {
  const findAndUpdate = (list) => {
    for (const item of list) {
      if (item.id === nodeData.id) {
        item.name = nodeData.name
        return true
      }
      if (item.children?.length && findAndUpdate(item.children)) return true
    }
    return false
  }
  findAndUpdate(dataSource.value)
}

// 重命名节点（调 API）
function editNode(nodeData) {
  usePcPictureApi().saveOrUpdateTree({ id: nodeData.id, name: nodeData.name }).then(() => {
    updateNodeInTree(nodeData)
    ElMessage.success('节点重命名成功')
  })
}

// 弹出重命名对话框
function openReNodeNameDialog(data) {
  editNodeForm.value?.open(data)
}

// 重命名对话框提交回调
function handleDialogSubmit(formData) {
  editNode(formData)
}

// 弹出添加子节点对话框
function append(data) {
  addNodeForm.value?.open(data)
}

// 添加子节点对话框提交回调
function appendAndSubmit({ name, parentNode }) {
  const parent_id = parentNode?.id ?? null
  usePcPictureApi().saveOrUpdateTree({ parent_id, name }).then((res) => {
    const newId = res.data?.id
    // 保留展开状态并本地写入
    if (parent_id !== null) {
      const findParent = (list) => {
        for (const item of list) {
          if (item.id === parent_id) {
            if (!item.children) item.children = []
            item.children.push({ id: newId, name, children: [] })
            // 保持父节点展开
            if (!expandedKeys.value.includes(parent_id)) {
              expandedKeys.value.push(parent_id)
            }
            return true
          }
          if (item.children?.length && findParent(item.children)) return true
        }
        return false
      }
      findParent(dataSource.value)
    } else {
      dataSource.value.push({ id: newId, name, children: [] })
    }
    ElMessage.success('节点添加成功')
    nextTick(() => { treeRef.value?.filter(filterText.value) })
  })
}

// 添加根节点（快捷，直接弹对话框并传 null 作为 parent）
function appendRootNode() {
  addNodeForm.value?.open(null)
}

// 删除节点
function remove(data) {
  ElMessageBox.confirm('删除该节点会同时删除其下所有素材，是否继续？', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    usePcPictureApi().deletedTree({ id: data.id }).then(() => {
      ElMessage.success('删除成功')
      getAllTree()
    })
  })
}

// 打开添加素材对话框
function openPictureDialog(data) {
  addPictureForm.value?.open(data)
}

// 素材保存成功，刷新右侧列表
function onPictureSaved() {
  pictureByTreeId()
}

onMounted(() => { getAllTree() })

defineExpose({ getAllTree, pictureByTreeId })
</script>

<style lang="scss" scoped>
.picture-tree {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.tree-node-row {
  display: flex;
  align-items: center;
  width: 100%;
  justify-content: space-between;
  overflow: hidden;
}

.tree-node-label {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 13px;
}

.tree-node-actions {
  flex-shrink: 0;
  display: flex;
  gap: 2px;
}
</style>

<template>
  <div class="app-container h100">
    <el-card style="height: 100%;" :body-style="{ height: 'calc(100% - 56px)', display: 'flex', gap: '12px' }">
      <!-- 左侧：素材树 -->
      <div style="width: 220px; border-right: 1px solid #eee; padding-right: 12px; overflow-y: auto; flex-shrink: 0;">
        <PictureTree ref="treeRef" @node-click="handleTreeNodeClick"/>
      </div>

      <!-- 右侧：素材列表 -->
      <div style="flex: 1; overflow-y: auto;">
        <div class="mb10">
          <el-input
              v-model="state.listQuery.name"
              placeholder="素材名称查询"
              clearable
              style="width: 200px"
              @keyup.enter="search"
          />
          <el-button type="primary" class="ml10" @click="search">查询</el-button>
          <el-button type="success" class="ml10" @click="openAdd">新增素材</el-button>
          <span v-if="state.currentTreeNode" class="ml10" style="font-size: 13px; color: #909399;">
            当前节点：{{ state.currentTreeNode.name }}
          </span>
        </div>

        <!-- 图片网格 -->
        <div class="picture-grid">
          <div
              v-for="pic in state.listData"
              :key="pic.id"
              class="picture-item"
          >
            <el-image
                :src="getPicUrl(pic)"
                fit="contain"
                style="width: 100%; height: 100px;"
                :preview-src-list="[getPicUrl(pic)]"
                preview-teleported
            />
            <div class="picture-item__name">{{ pic.name }}</div>
            <div class="picture-item__actions">
              <el-button size="small" type="warning" @click="openEdit(pic)">编辑</el-button>
              <el-button size="small" type="danger" @click="deleted(pic)">删除</el-button>
            </div>
          </div>
        </div>

        <el-empty v-if="state.listData.length === 0" description="暂无素材"/>

        <el-pagination
            v-model:current-page="state.listQuery.page"
            v-model:page-size="state.listQuery.pageSize"
            :total="state.total"
            layout="prev, pager, next, total"
            style="margin-top: 12px"
            @current-change="getList"
        />
      </div>
    </el-card>

    <PictureEdit
        v-if="state.showEditDialog"
        v-model:visible="state.showEditDialog"
        :picture="state.editRow"
        @saved="onSaved"
    />
  </div>
</template>

<script setup name="pictureMaterialLibrary">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { usePcPictureApi } from '/@/api/usePcAutoApi/pcPicture.js'
import { getBaseApiUrl } from '/@/utils/config'
import PictureTree from '/@/views/pcAutoTest/component/pictureMaterialLibrary/pictureTree.vue'
import PictureEdit from '/@/views/pcAutoTest/component/pictureMaterialLibrary/pictureEdit.vue'

const treeRef = ref()
const pictureApi = usePcPictureApi()

const state = reactive({
  listData: [],
  total: 0,
  listQuery: { page: 1, pageSize: 20, name: '', tree_id: null },
  currentTreeNode: null,
  showEditDialog: false,
  editRow: null,
})

const getPicUrl = (pic) => {
  const url = pic.file_path || pic.url || ''
  if (!url) return ''
  return url.startsWith('http') ? url : `${getBaseApiUrl()}/${url}`
}

const search = () => {
  state.listQuery.page = 1
  getList()
}

const getList = () => {
  pictureApi.getPictureList(state.listQuery).then((res) => {
    state.listData = res.data.rows || []
    state.total = res.data.rowTotal || 0
  })
}

const handleTreeNodeClick = (node) => {
  state.currentTreeNode = node
  state.listQuery.tree_id = node.id
  state.listQuery.page = 1
  getList()
}

const openAdd = () => {
  state.editRow = null
  state.showEditDialog = true
}

const openEdit = (row) => {
  state.editRow = row
  state.showEditDialog = true
}

const onSaved = () => {
  getList()
  treeRef.value?.fetchTree()
}

const deleted = (pic) => {
  ElMessageBox.confirm('是否删除该素材?', '提示', {
    confirmButtonText: '确认', cancelButtonText: '取消', type: 'warning',
  }).then(() => {
    pictureApi.deleted({ id: pic.id }).then(() => {
      ElMessage.success('删除成功')
      getList()
    })
  })
}

onMounted(() => { getList() })
</script>

<style lang="scss" scoped>
.picture-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 12px;
}

.picture-item {
  border: 1px solid #eee;
  border-radius: 6px;
  padding: 8px;
  text-align: center;
  transition: box-shadow 0.2s;

  &:hover {
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.12);
  }

  .picture-item__name {
    font-size: 12px;
    color: #606266;
    margin: 4px 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .picture-item__actions {
    display: flex;
    gap: 4px;
    justify-content: center;
  }
}
</style>

<template>
  <div class="app-container">
    <el-card>
      <div class="mb15">
        <el-input
            v-model="state.listQuery.name"
            placeholder="素材名称查询"
            clearable
            style="width: 200px"
            @keyup.enter="search"
        />
        <el-button type="primary" class="ml10" @click="search">查询</el-button>
        <el-button type="success" class="ml10" @click="openAdd">新增素材</el-button>
      </div>

      <z-table
          ref="tableRef"
          :columns="state.columns"
          :data="state.listData"
          v-model:page-size="state.listQuery.pageSize"
          v-model:page="state.listQuery.page"
          :total="state.total"
          @pagination-change="getList"
      />
    </el-card>

    <!-- 新增/编辑弹窗 -->
    <PictureEdit
        v-if="state.showEditDialog"
        v-model:visible="state.showEditDialog"
        :picture="state.editRow"
        @saved="onSaved"
    />
  </div>
</template>

<script setup name="pcAutoPictureList">
import { h, onMounted, reactive, ref } from 'vue'
import { ElButton, ElImage, ElMessage, ElMessageBox } from 'element-plus'
import { usePcPictureApi } from '/@/api/usePcAutoApi/pcPicture.js'
import { getBaseApiUrl } from '/@/utils/config'
import PictureEdit from '/@/views/pcAutoTest/component/pictureMaterialLibrary/pictureEdit.vue'

const tableRef = ref()
const pictureApi = usePcPictureApi()

const getPicUrl = (url) => {
  if (!url) return ''
  return url.startsWith('http') ? url : `${getBaseApiUrl()}/${url}`
}

const state = reactive({
  listData: [],
  total: 0,
  listQuery: { page: 1, pageSize: 20, name: '' },
  showEditDialog: false,
  editRow: null,
  columns: [
    { label: '序号', columnType: 'index', align: 'center', width: 'auto' },
    {
      key: 'image_url', label: '素材图片', align: 'center', width: '120',
      render: ({ row }) => h(ElImage, {
        src: getPicUrl(row.image_url),
        fit: 'contain',
        previewSrcList: [getPicUrl(row.image_url)],
        previewTeleported: true,
        style: { width: '80px', height: '55px' },
      }),
    },
    { key: 'name', label: '素材名称', width: '' },
    { key: 'tree_name', label: '所属树节点', align: 'center', width: '' },
    { key: 'source_type', label: '来源类型', align: 'center', width: '100' },
    { key: 'creation_date', label: '创建时间', align: 'center', width: '150' },
    { key: 'created_by_name', label: '创建人', align: 'center', width: '' },
    {
      label: '操作', fixed: 'right', align: 'center', width: '150',
      render: ({ row }) => h('div', null, [
        h(ElButton, { type: 'warning', onClick: () => openEdit(row) }, () => '编辑'),
        h(ElButton, { type: 'danger', onClick: () => deleted(row) }, () => '删除'),
      ]),
    },
  ],
})

const search = () => {
  state.listQuery.page = 1
  getList()
}

const getList = () => {
  tableRef.value.openLoading()
  pictureApi.getList(state.listQuery)
    .then((res) => {
      state.listData = res.data.rows
      state.total = res.data.rowTotal
    })
    .finally(() => tableRef.value.closeLoading())
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
}

const deleted = (row) => {
  ElMessageBox.confirm('是否删除该素材?', '提示', {
    confirmButtonText: '确认', cancelButtonText: '取消', type: 'warning',
  }).then(() => {
    pictureApi.deletePicture({ id: row.id }).then(() => {
      ElMessage.success('删除成功')
      getList()
    })
  })
}

onMounted(() => { getList() })
</script>

<style lang="scss" scoped></style>

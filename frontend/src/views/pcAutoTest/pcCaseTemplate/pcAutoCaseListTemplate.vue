<template>
  <div class="app-container">
    <el-card>
      <div class="mb15">
        <el-input
            v-model="state.listQuery.title"
            placeholder="请输入用例名称"
            style="max-width: 200px"
            clearable
            @keyup.enter="search"
        />
        <el-button type="primary" class="ml10" @click="search">查询</el-button>
        <el-button type="success" class="ml10" @click="onOpenSaveOrUpdate(null)">新增</el-button>
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
  </div>
</template>

<script setup name="pcAutoCaseListTemplate">
import { h, onMounted, reactive, ref } from 'vue'
import { ElButton, ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import { usePcTestCaseApi } from '/@/api/usePcAutoApi/pcTestCase'

const tableRef = ref()
const router = useRouter()

const state = reactive({
  listData: [],
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    title: '',
    is_template: true,
    created_by: '',
    prioritys: [],
    module: null,
  },
  columns: [
    { label: '序号', columnType: 'index', width: 'auto', align: 'center' },
    {
      key: 'name', label: '模板名称', width: '',
      render: ({ row }) => h(ElButton, {
        link: true, type: 'primary',
        onClick: () => onOpenSaveOrUpdate(row),
      }, () => row.name),
    },
    { key: 'remarks', label: '备注', width: '', align: 'center' },
    { key: 'updation_date', label: '更新时间', width: '150', align: 'center' },
    { key: 'updated_by_name', label: '更新人', width: '', align: 'center' },
    { key: 'creation_date', label: '创建时间', width: '150', align: 'center' },
    { key: 'created_by_name', label: '创建人', width: '', align: 'center' },
    {
      label: '操作', fixed: 'right', align: 'center', width: '150',
      render: ({ row }) => h('div', null, [
        h(ElButton, { type: 'warning', onClick: () => onOpenSaveOrUpdate(row) }, () => '编辑'),
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
  tableRef.value?.openLoading()
  usePcTestCaseApi().getPcCaseList(state.listQuery)
    .then((res) => {
      state.listData = res.data.rows
      state.total = res.data.rowTotal
    })
    .finally(() => tableRef.value?.closeLoading())
}

const onOpenSaveOrUpdate = (row) => {
  const query = { editType: row ? 'update' : 'save' }
  if (row) query.id = row.id
  router.push({ name: 'editPcAutoCaseTemplate', query })
}

const deleted = (row) => {
  ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    usePcTestCaseApi().deleteCase({ id: row.id }).then(() => {
      ElMessage.success('删除成功')
      getList()
    })
  })
}

onMounted(() => { getList() })
</script>

<style lang="scss" scoped></style>

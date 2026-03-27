<template>
  <div class="app-container">
    <el-card>
      <div class="mb15">
        <el-input
            v-model="state.listQuery.name"
            placeholder="请输入计划名称"
            style="max-width: 200px"
            clearable
        />
        <el-button type="primary" class="ml10" @click="search">查询</el-button>
        <el-button type="success" class="ml10" @click="toEdit(null)">新增</el-button>
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

    <PcCaseExecute
        v-if="state.showExecuteDialog"
        v-model:visible="state.showExecuteDialog"
        :case-ids="state.executeCaseIds"
    />
  </div>
</template>

<script setup name="pcAutoPlanList">
import { h, onMounted, reactive, ref } from 'vue'
import { ElButton, ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import { usePcPlanApi } from '/@/api/usePcAutoApi/pcPlan.js'
import PcCaseExecute from '/@/views/pcAutoTest/form/PcCaseExecute.vue'

const tableRef = ref()
const router = useRouter()
const planApi = usePcPlanApi()

const state = reactive({
  listData: [],
  total: 0,
  listQuery: { page: 1, pageSize: 20, name: '' },
  showExecuteDialog: false,
  executeCaseIds: [],
  columns: [
    { label: '序号', columnType: 'index', width: 'auto', align: 'center' },
    {
      key: 'name', label: '计划名称', width: '',
      render: ({ row }) => h(ElButton, {
        link: true, type: 'primary',
        onClick: () => toEdit(row),
      }, () => row.name),
    },
    { key: 'remarks', label: '备注', width: '', align: 'center' },
    { key: 'case_count', label: '用例数', width: '', align: 'center' },
    { key: 'updation_date', label: '更新时间', width: '150', align: 'center' },
    { key: 'updated_by_name', label: '更新人', width: '', align: 'center' },
    {
      label: '操作', fixed: 'right', align: 'center', width: '240',
      render: ({ row }) => h('div', null, [
        h(ElButton, { type: 'primary', onClick: () => runPlan(row) }, () => '执行'),
        h(ElButton, { type: 'info', onClick: () => viewReport(row) }, () => '报告'),
        h(ElButton, { type: 'warning', onClick: () => toEdit(row) }, () => '编辑'),
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
  planApi.getList(state.listQuery)
    .then((res) => {
      state.listData = res.data.rows
      state.total = res.data.rowTotal
    })
    .finally(() => tableRef.value.closeLoading())
}

const toEdit = (row) => {
  const query = { editType: row ? 'update' : 'save' }
  if (row) query.id = row.id
  router.push({ name: 'editPcPlan', query })
}

const runPlan = (row) => {
  planApi.runPlan({ id: row.id }).then((res) => {
    ElMessage.success('计划已提交执行')
    const reportId = res.data?.report_id
    if (reportId) {
      router.push({ name: 'pcPlanReportList', query: { plan_id: row.id } })
    }
  })
}

const viewReport = (row) => {
  router.push({ name: 'pcPlanReportList', query: { plan_id: row.id } })
}

const deleted = (row) => {
  ElMessageBox.confirm('是否删除该计划?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    planApi.deleted({ id: row.id }).then(() => {
      ElMessage.success('删除成功')
      getList()
    })
  })
}

onMounted(() => { getList() })
</script>

<style lang="scss" scoped></style>

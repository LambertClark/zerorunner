<template>
  <div class="app-container">
    <el-card>
      <div class="mb15">
        <el-button type="primary" @click="search">刷新</el-button>
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

<script setup name="pcPlanReportList">
import { h, onMounted, reactive, ref } from 'vue'
import { ElButton, ElMessage, ElMessageBox, ElTag } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'
import { usePcPlanApi } from '/@/api/usePcAutoApi/pcPlan.js'

const tableRef = ref()
const route = useRoute()
const router = useRouter()

const state = reactive({
  listData: [],
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    plan_id: null,
  },
  columns: [
    { label: '序号', columnType: 'index', align: 'center', width: 'auto' },
    {
      key: 'name', label: '报告名称', width: '',
      render: ({ row }) => h(ElButton, {
        link: true, type: 'primary',
        onClick: () => viewReport(row),
      }, () => row.name),
    },
    {
      key: 'success', label: '结果', align: 'center', width: '100',
      render: ({ row }) => h(ElTag, {
        type: row.success ? 'success' : 'danger',
      }, () => row.success ? '通过' : '不通过'),
    },
    { key: 'step_count', label: '步骤总数', align: 'center', width: '' },
    { key: 'duration', label: '耗时(s)', align: 'center', width: '' },
    { key: 'start_time', label: '开始时间', align: 'center', width: '150' },
    { key: 'exec_user_name', label: '执行人', align: 'center', width: '' },
    {
      label: '操作', fixed: 'right', align: 'center', width: '140',
      render: ({ row }) => h('div', null, [
        h(ElButton, { type: 'primary', onClick: () => viewReport(row) }, () => '查看'),
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
  usePcPlanApi().getPlanReportList(state.listQuery)
    .then((res) => {
      state.listData = res.data.rows
      state.total = res.data.rowTotal
    })
    .finally(() => tableRef.value.closeLoading())
}

const viewReport = (row) => {
  router.push({ name: 'pcReportDetail', query: { id: row.id } })
}

const deleted = (row) => {
  ElMessageBox.confirm('是否删除该报告?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    usePcPlanApi().deletedPlanReport({ id: row.id }).then(() => {
      ElMessage.success('删除成功')
      getList()
    })
  })
}

onMounted(() => {
  state.listQuery.plan_id = route.query.plan_id || null
  getList()
})
</script>

<style lang="scss" scoped></style>

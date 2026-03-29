<template>
  <div class="app-container">
    <el-card>
      <div class="mb15">
        <el-input
            v-model="state.listQuery.title"
            placeholder="请输入计划名称"
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

<script setup name="pcAutoPlanList">
import { h, onMounted, reactive, ref } from 'vue'
import { ElButton, ElMessage, ElMessageBox } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'
import { usePcPlanApi } from '/@/api/usePcAutoApi/pcPlan'
import { usePcTestCaseApi } from '/@/api/usePcAutoApi/pcTestCase'

const tableRef = ref()
const route = useRoute()
const router = useRouter()

const state = reactive({
  listData: [],
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    title: '',
    desc: '',
    enabled_flag: null,
  },
  columns: [
    { label: '序号', columnType: 'index', width: 'auto', align: 'center' },
    {
      key: 'title', label: '计划名称', width: '',
      render: ({ row }) => h(ElButton, {
        link: true, type: 'primary',
        onClick: () => onOpenSaveOrUpdate(row),
      }, () => row.title || row.name),
    },
    { key: 'desc', label: '描述', width: '', align: 'center' },
    { key: 'case_count', label: '用例数', width: '', align: 'center' },
    { key: 'updation_date', label: '更新时间', width: '150', align: 'center' },
    { key: 'updated_by_name', label: '更新人', width: '', align: 'center' },
    {
      label: '操作', fixed: 'right', align: 'center', width: '260',
      render: ({ row }) => h('div', null, [
        h(ElButton, { type: 'primary', onClick: () => runPlan(row) }, () => '执行'),
        h(ElButton, { type: 'info', onClick: () => viewDetail(row) }, () => '详情'),
        h(ElButton, { type: 'success', onClick: () => copyPlan(row) }, () => '复制'),
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
  usePcPlanApi().getPcPlanList(state.listQuery)
    .then((res) => {
      state.listData = res.data.rows
      state.total = res.data.rowTotal
    })
    .finally(() => tableRef.value?.closeLoading())
}

const onOpenSaveOrUpdate = (row) => {
  const query = { editType: row ? 'update' : 'save' }
  if (row) query.id = row.id
  router.push({ name: 'editPcAutoPlan', query })
}

const viewDetail = (row) => {
  usePcPlanApi().getPcPlanDetail({ id: row.id }).then((res) => {
    router.push({ name: 'editPcAutoPlan', query: { id: row.id, editType: 'update' } })
  })
}

const copyPlan = (row) => {
  usePcPlanApi().copyPcPlan({ id: row.id }).then(() => {
    ElMessage.success('复制成功')
    getList()
  })
}

const runPlan = (row) => {
  usePcPlanApi().runPlanCases({ id: row.id }).then((res) => {
    ElMessage.success('计划已提交执行')
    const reportId = res.data?.report_id
    if (reportId) {
      router.push({ name: 'pcPlanReportList', query: { plan_id: row.id } })
    }
  })
}

const deleted = (row) => {
  ElMessageBox.confirm('是否删除该计划?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    usePcPlanApi().deletePcPlan({ id: row.id }).then(() => {
      ElMessage.success('删除成功')
      getList()
    })
  })
}

onMounted(() => { getList() })
</script>

<style lang="scss" scoped></style>

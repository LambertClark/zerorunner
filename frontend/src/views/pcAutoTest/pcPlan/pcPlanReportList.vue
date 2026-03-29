<template>
  <div class="app-container">
    <el-card>
      <div class="mb15">
        <el-input
            v-model="state.listQuery.name"
            placeholder="报告名称查询"
            clearable
            style="width: 200px"
            @keyup.enter="search"
        />
        <el-select
            v-model="state.listQuery.status"
            placeholder="状态"
            clearable
            style="width: 120px; margin-left: 10px"
        >
          <el-option label="通过" value="SUCCESS"/>
          <el-option label="失败" value="FAILURE"/>
          <el-option label="错误" value="ERROR"/>
        </el-select>
        <el-input
            v-model="state.listQuery.exec_user_name"
            placeholder="执行人"
            clearable
            style="width: 140px; margin-left: 10px"
        />
        <el-button type="primary" class="ml10" @click="search">查询</el-button>
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

    <!-- 报告详情弹窗 -->
    <el-dialog
        v-model="state.showDetailDialog"
        title="计划报告详情"
        width="80%"
        top="5vh"
        destroy-on-close
    >
      <div v-if="state.currentDetail">
        <el-descriptions :column="2" border size="small">
          <el-descriptions-item label="报告名称">{{ state.currentDetail.name }}</el-descriptions-item>
          <el-descriptions-item label="执行状态">
            <el-tag :type="state.currentDetail.success ? 'success' : 'danger'">
              {{ state.currentDetail.success ? '通过' : '不通过' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="用例总数">{{ state.currentDetail.case_count }}</el-descriptions-item>
          <el-descriptions-item label="成功数">{{ state.currentDetail.success_count }}</el-descriptions-item>
          <el-descriptions-item label="耗时(s)">{{ state.currentDetail.duration }}</el-descriptions-item>
          <el-descriptions-item label="执行人">{{ state.currentDetail.exec_user_name }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>

    <!-- 新增/编辑弹窗 -->
    <el-dialog
        v-model="state.showSaveDialog"
        :title="state.saveForm.id ? '编辑报告' : '新增报告'"
        width="500px"
        destroy-on-close
    >
      <el-form :model="state.saveForm" label-width="90px" size="small">
        <el-form-item label="报告名称">
          <el-input v-model="state.saveForm.name" placeholder="报告名称"/>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="state.showSaveDialog = false">取消</el-button>
        <el-button type="primary" @click="saveOrUpdateReport">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="pcPlanReportList">
import { h, onMounted, reactive, ref } from 'vue'
import { ElButton, ElMessage, ElMessageBox, ElTag } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'
import { usePcPlanReportApi } from '/@/api/usePcAutoApi/pcPlan'

const tableRef = ref()
const route = useRoute()
const router = useRouter()

const state = reactive({
  listData: [],
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    name: '',
    status: '',
    exec_user_name: '',
    plan_id: null,
  },
  showDetailDialog: false,
  currentDetail: null,
  showSaveDialog: false,
  saveForm: { id: null, name: '' },
  columns: [
    { label: '序号', columnType: 'index', align: 'center', width: 'auto' },
    {
      key: 'name', label: '报告名称', width: '',
      render: ({ row }) => h(ElButton, {
        link: true, type: 'primary',
        onClick: () => viewDetail(row),
      }, () => row.name),
    },
    {
      key: 'success', label: '结果', align: 'center', width: '100',
      render: ({ row }) => h(ElTag, {
        type: row.success ? 'success' : 'danger',
      }, () => row.success ? '通过' : '不通过'),
    },
    { key: 'case_count', label: '用例总数', align: 'center', width: '' },
    { key: 'success_count', label: '成功数', align: 'center', width: '' },
    { key: 'duration', label: '耗时(s)', align: 'center', width: '' },
    { key: 'start_time', label: '开始时间', align: 'center', width: '150' },
    { key: 'exec_user_name', label: '执行人', align: 'center', width: '' },
    {
      label: '操作', fixed: 'right', align: 'center', width: '180',
      render: ({ row }) => h('div', null, [
        h(ElButton, { type: 'primary', onClick: () => viewDetail(row) }, () => '详情'),
        h(ElButton, { type: 'warning', onClick: () => openSaveDialog(row) }, () => '编辑'),
        h(ElButton, { type: 'danger', onClick: () => deletePlanReport(row) }, () => '删除'),
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
  usePcPlanReportApi().getPcPlanReportList(state.listQuery)
    .then((res) => {
      state.listData = res.data.rows
      state.total = res.data.rowTotal
    })
    .finally(() => tableRef.value?.closeLoading())
}

const viewDetail = (row) => {
  usePcPlanReportApi().getPcPlanReportDetail({ id: row.id }).then((res) => {
    state.currentDetail = res.data
    state.showDetailDialog = true
  })
}

const openSaveDialog = (row) => {
  state.saveForm = { id: row?.id ?? null, name: row?.name ?? '' }
  state.showSaveDialog = true
}

const saveOrUpdateReport = () => {
  usePcPlanReportApi().saveOrUpdateReport(state.saveForm).then(() => {
    ElMessage.success('保存成功')
    state.showSaveDialog = false
    getList()
  })
}

const deletePlanReport = (row) => {
  ElMessageBox.confirm('是否删除该报告?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    usePcPlanReportApi().deletePcPlanReport({ id: row.id }).then(() => {
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

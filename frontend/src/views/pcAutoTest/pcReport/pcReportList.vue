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
  </div>
</template>

<script setup name="pcReportList">
import { h, onMounted, reactive, ref } from 'vue'
import { ElButton, ElMessage, ElMessageBox, ElTag } from 'element-plus'
import { useRouter } from 'vue-router'
import { usePcReportApi } from '/@/api/usePcAutoApi/pcReport'

const tableRef = ref()
const router = useRouter()

const state = reactive({
  listData: [],
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    id: null,
    name: '',
    min_and_max: null,
    exec_user_name: '',
    status: '',
    ids: [],
  },
  columns: [
    { label: '序号', columnType: 'index', align: 'center', width: 'auto' },
    {
      key: 'name', label: '报告名称', align: 'center', width: '',
      render: ({ row }) => h(ElButton, {
        link: true, type: 'primary',
        onClick: () => onOpenReport(row),
      }, () => row.name),
    },
    {
      key: 'success', label: '运行结果', align: 'center', width: '100',
      render: ({ row }) => h(ElTag, {
        type: row.success ? 'success' : 'danger',
      }, () => row.success ? '通过' : '不通过'),
    },
    { key: 'step_count', label: '步骤总数', align: 'center', width: '' },
    { key: 'success_count', label: '成功数', align: 'center', width: '' },
    { key: 'duration', label: '耗时(s)', align: 'center', width: '' },
    { key: 'start_time', label: '开始时间', align: 'center', width: '150' },
    { key: 'exec_user_name', label: '执行人', align: 'center', width: '' },
    { key: 'error_msg', label: '错误信息', align: 'center', width: '180' },
    {
      label: '操作', fixed: 'right', align: 'center', width: '140',
      render: ({ row }) => h('div', null, [
        h(ElButton, { type: 'primary', onClick: () => onOpenReport(row) }, () => '查看'),
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
  usePcReportApi().getList(state.listQuery)
    .then((res) => {
      state.listData = res.data.rows
      state.total = res.data.rowTotal
    })
    .finally(() => tableRef.value?.closeLoading())
}

const onOpenReport = (row) => {
  router.push({ name: 'pcAutoCaseReportDetail', query: { id: row.id } })
}

const deleted = (row) => {
  ElMessageBox.confirm('是否删除该报告, 是否继续?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    usePcReportApi().deleted({ id: row.id }).then(() => {
      ElMessage.success('删除成功')
      getList()
    })
  })
}

onMounted(() => { getList() })
</script>

<style lang="scss" scoped></style>

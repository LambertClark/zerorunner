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
        <el-select
            v-model="state.listQuery.case_category"
            placeholder="选择用例分类"
            clearable
            style="max-width: 160px; margin-left: 10px"
        >
          <el-option
              v-for="opt in caseCategoryOptions"
              :key="opt.value"
              :label="opt.label"
              :value="opt.value"
          />
        </el-select>
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

    <PcCaseExecute ref="executeRef" @open-report="onOpenReport"/>
  </div>
</template>

<script setup name="pcAutoCase">
import { h, onMounted, reactive, ref } from 'vue'
import { ElButton, ElMessage, ElMessageBox, ElTag } from 'element-plus'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { usePcTestCaseApi } from '/@/api/usePcAutoApi/pcTestCase'
import PcCaseExecute from '/@/views/pcAutoTest/form/PcCaseExecute.vue'
import { useUserInfo } from '/@/stores/userInfo'

const caseCategoryOptions = [
  { value: 'release', label: '发版用例' },
  { value: 'sit', label: 'SIT用例' },
  { value: 'performance', label: '性能用例' },
]

const caseCategoryMap = {
  release: '发版用例',
  sit: 'SIT用例',
  performance: '性能用例',
}

const formatCaseCategory = (val) => caseCategoryMap[val] || val

const tableRef = ref()
const executeRef = ref()
const router = useRouter()
const { userInfos } = storeToRefs(useUserInfo())

const state = reactive({
  listData: [],
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    title: '',
    is_template: false,
    created_by: '',
    prioritys: [],
    module: null,
    case_category: '',
  },
  columns: [
    { label: '序号', columnType: 'index', width: 'auto', align: 'center' },
    {
      key: 'title', label: '用例名称', width: '',
      render: ({ row }) => h(ElButton, {
        link: true, type: 'primary',
        onClick: () => onOpenSaveOrUpdate(row),
      }, () => row.title),
    },
    {
      key: 'case_category', label: '用例分类', width: '100', align: 'center',
      render: ({ row }) => h(ElTag, { size: 'small' }, () => formatCaseCategory(row.case_category)),
    },
    { key: 'desc', label: '备注', width: '', align: 'center' },
    { key: 'updation_date', label: '更新时间', width: '150', align: 'center' },
    { key: 'updated_by_name', label: '更新人', width: '', align: 'center' },
    { key: 'creation_date', label: '创建时间', width: '150', align: 'center' },
    { key: 'created_by_name', label: '创建人', width: '', align: 'center' },
    {
      label: '操作', fixed: 'right', align: 'center', width: '200',
      render: ({ row }) => h('div', null, [
        h(ElButton, { type: 'primary', onClick: () => onOpenRunConfigDialog(row) }, () => '运行'),
        h(ElButton, { type: 'warning', onClick: () => onOpenSaveOrUpdate(row) }, () => '编辑'),
        h(ElButton, {
          type: 'danger',
          disabled: !canDeleteCase(row),
          onClick: () => deleted(row),
        }, () => '删除'),
      ]),
    },
  ],
})

const canDeleteCase = (row) => row.created_by === userInfos.value?.id

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
  if (row) {
    query.id = row.id
  } else {
    query.timestamp = new Date().getTime()
  }
  if (!router.hasRoute('editPcAutoCase')) {
    ElMessage.warning('未配置编辑页面路由，请在菜单管理新增隐藏菜单：/pcAutoTest/pcCase/edit')
    return
  }
  router.push({ name: 'editPcAutoCase', query }).catch(() => {
    ElMessage.warning('编辑页面路由不可用，请检查菜单路由名称和路径配置')
  })
}

const onOpenRunConfigDialog = (row) => {
  executeRef.value?.openDialog(row)
}

const onOpenReport = (reportId) => {
  if (reportId) {
    router.push({ name: 'pcAutoCaseReportDetail', query: { id: reportId } })
  }
}

const deleted = (row) => {
  if (!canDeleteCase(row)) {
    ElMessage.warning('仅允许用例创建人删除')
    return
  }
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

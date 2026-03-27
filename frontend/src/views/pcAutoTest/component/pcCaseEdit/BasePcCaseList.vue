<template>
  <div class="app-container">
    <el-card>
      <div class="mb15">
        <el-input
            v-model="state.listQuery.name"
            placeholder="请输入用例名称"
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

    <!-- 执行弹窗 -->
    <PcCaseExecute
        v-if="state.showExecuteDialog"
        v-model:visible="state.showExecuteDialog"
        :case-ids="state.executeCaseIds"
        @run-success="onRunSuccess"
    />
  </div>
</template>

<script setup name="BasePcCaseList">
import { h, onMounted, reactive, ref } from 'vue'
import { ElButton, ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import PcCaseExecute from '/@/views/pcAutoTest/form/PcCaseExecute.vue'

const props = defineProps({
  // 用于区分是"普通用例"还是"模板用例"
  caseType: {
    type: String,
    default: 'case', // 'case' | 'template'
  },
  // 编辑页路由名
  editRouteName: {
    type: String,
    required: true,
  },
  // API 实例（由父页面传入，避免在公共组件中硬编码）
  api: {
    type: Object,
    required: true,
  },
  // 是否显示"运行"按钮（模板用例不需要）
  showRun: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['run-success'])

const tableRef = ref()
const router = useRouter()

const state = reactive({
  listData: [],
  total: 0,
  listQuery: {
    page: 1,
    pageSize: 20,
    name: '',
  },
  showExecuteDialog: false,
  executeCaseIds: [],
  columns: buildColumns(),
})

function buildColumns() {
  const cols = [
    { label: '序号', columnType: 'index', width: 'auto', show: true },
    {
      key: 'name', label: '用例名称', width: '', show: true,
      render: ({ row }) => h(ElButton, {
        link: true, type: 'primary',
        onClick: () => toEdit(row),
      }, () => row.name),
    },
    { key: 'remarks', label: '备注', width: '', align: 'center', show: true },
    { key: 'updation_date', label: '更新时间', width: '150', align: 'center', show: true },
    { key: 'updated_by_name', label: '更新人', width: '', align: 'center', show: true },
    { key: 'creation_date', label: '创建时间', width: '150', align: 'center', show: true },
    { key: 'created_by_name', label: '创建人', width: '', align: 'center', show: true },
    {
      label: '操作', fixed: 'right', width: props.showRun ? '200' : '150', align: 'center',
      render: ({ row }) => h('div', null, [
        props.showRun
          ? h(ElButton, {
              type: 'primary',
              onClick: () => openExecuteDialog(row),
            }, () => '运行')
          : null,
        h(ElButton, {
          type: 'warning',
          onClick: () => toEdit(row),
        }, () => '编辑'),
        h(ElButton, {
          type: 'danger',
          onClick: () => deleted(row),
        }, () => '删除'),
      ]),
    },
  ]
  return cols
}

const search = () => {
  state.listQuery.page = 1
  getList()
}

const getList = () => {
  tableRef.value.openLoading()
  const apiFn = props.caseType === 'template'
    ? props.api.getPcTemplateList
    : props.api.getList
  apiFn(state.listQuery)
    .then((res) => {
      state.listData = res.data.rows
      state.total = res.data.rowTotal
    })
    .finally(() => {
      tableRef.value.closeLoading()
    })
}

const toEdit = (row) => {
  const query = { editType: row ? 'update' : 'save' }
  if (row) query.id = row.id
  router.push({ name: props.editRouteName, query })
}

const openExecuteDialog = (row) => {
  state.executeCaseIds = [row.id]
  state.showExecuteDialog = true
}

const onRunSuccess = (reportId) => {
  emit('run-success', reportId)
}

const deleted = (row) => {
  ElMessageBox.confirm('是否删除该条数据, 是否继续?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    const apiFn = props.caseType === 'template'
      ? props.api.deletedTemplate
      : props.api.deleted
    apiFn({ id: row.id }).then(() => {
      ElMessage.success('删除成功')
      getList()
    })
  })
}

onMounted(() => {
  getList()
})

defineExpose({ getList })
</script>

<style lang="scss" scoped></style>

<template>
  <div>
    <el-dialog
        v-model="state.showReportDialog"
        title="报告详情"
        width="80%"
        destroy-on-close
        append-to-body
    >
      <!-- 报告统计 -->
      <el-card style="margin-bottom: 12px" v-if="state.statisticsData">
        <ReportStatistics
            :data="state.statisticsData"
            :start_time="state.start_time"
            :exec_user_name="state.exec_user_name"
        />
      </el-card>

      <!-- 步骤列表 -->
      <el-card>
        <div class="mb10">
          <el-input
              v-model="state.listQuery.name"
              placeholder="步骤名称查询"
              clearable
              style="width: 200px"
              @keyup.enter="searchDetail"
          />
          <el-button type="primary" class="ml10" @click="searchDetail">查询</el-button>
          <el-checkbox
              v-model="state.viewErrOrFailApiStatus"
              class="ml10"
              @change="viewErrOrFailApi"
          >
            只看失败/错误步骤
          </el-checkbox>
        </div>

        <z-table
            :columns="state.columns"
            :data="state.listData"
            :show-page="false"
            row-key="id"
        />
      </el-card>
    </el-dialog>
  </div>
</template>

<script setup name="UiReportDetail">
import { h, nextTick, reactive } from 'vue'
import { ElButton, ElTag, ElImage } from 'element-plus'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useUserInfo } from '/@/stores/userInfo'
import { usePcReportApi } from '/@/api/usePcAutoApi/pcReport'
import useMouseData from '/@/hooks/pcAutoTest/useMouseData'
import ReportStatistics from './uiReportStatistics.vue'

const props = defineProps({
  reportInfo: {
    type: Object,
    default: null,
  },
  isDebug: {
    type: Boolean,
    default: false,
  },
})

const router = useRouter()
const { operationTypeToZh } = useMouseData()
const userStores = useUserInfo()
const { userInfos } = storeToRefs(userStores)

const state = reactive({
  showReportDialog: false,
  report_id: null,
  start_time: '',
  exec_user_name: '',
  viewErrOrFailApiStatus: false,
  listQuery: {
    report_id: null,
    name: '',
    status_list: [],
    page: 1,
    pageSize: 200,
  },
  listData: [],
  reportData: null,
  statisticsData: null,
  statQuery: {},
  screenshotUrlList: [],
  columns: [
    { label: 'N', columnType: 'index', align: 'center', width: 'auto' },
    {
      key: 'name', label: '步骤名称', width: '',
      render: ({ row }) => h(ElButton, {
        link: true, type: 'primary',
        onClick: () => viewDetail(row),
      }, () => row.name),
    },
    {
      key: 'operation_type', label: '操作类型', align: 'center', width: '160',
      render: ({ row }) => h('span', operationTypeToZh[row.operation_type] || row.operation_type || '-'),
    },
    { key: 'duration', label: '耗时(s)', align: 'center', width: '100' },
    {
      key: 'is_template', label: '模板步骤', align: 'center', width: '90',
      render: ({ row }) => h(ElTag, { type: row.is_template ? 'warning' : 'info', size: 'small' },
        () => row.is_template ? '是' : '否'),
    },
    {
      key: 'operation_state', label: '状态', align: 'center', width: '100',
      render: ({ row }) => h(ElTag, {
        type: statusTagType(row.operation_state),
      }, () => row.operation_state || '-'),
    },
    { key: 'error_type', label: '错误类型', align: 'center', width: '120' },
    {
      key: 'state_image', label: '执行截图', align: 'center', width: '120',
      render: ({ row }) => row.state_image
        ? h(ElImage, {
            src: row.state_image,
            fit: 'contain',
            previewSrcList: [row.state_image],
            previewTeleported: true,
            style: { width: '80px', height: '55px' },
          })
        : h('span', '-'),
    },
    { key: 'error_msg', label: '错误信息', width: '200', showTooltip: true },
  ],
})

const statusTagType = (status) => {
  const map = { SUCCESS: 'success', FAILURE: 'danger', ERROR: 'danger', SKIP: 'info' }
  return map[status] || 'info'
}

const initReport = () => {
  state.report_id = props.reportInfo?.report_id || props.reportInfo?.id || null
  state.start_time = props.reportInfo?.start_time || ''
  state.exec_user_name = props.reportInfo?.exec_user_name || ''
  if (state.report_id) {
    state.listQuery.report_id = state.report_id
    getDetails()
    getStatistics()
  }
}

const getDetails = () => {
  usePcReportApi().getReportDetail(state.listQuery).then((res) => {
    state.listData = res.data?.rows || res.data || []
    state.screenshotUrlList = state.listData
      .filter((s) => s.state_image)
      .map((s) => s.state_image)
  })
}

const searchDetail = () => {
  state.listQuery.page = 1
  getDetails()
}

const viewErrOrFailApi = (checked) => {
  if (checked) {
    state.listQuery.status_list = ['ERROR', 'FAILURE']
  } else {
    state.listQuery.status_list = []
  }
  getDetails()
}

const getStatistics = () => {
  usePcReportApi().getReportStatistics({ report_id: state.report_id }).then((res) => {
    state.statisticsData = res.data
  })
}

const viewDetail = (row) => {
  // 查看步骤详情，可扩展
}

const getChildrenData = (row) => {
  return row.children || []
}

const toApiInfo = (row) => {
  router.push({ name: 'pcCaseEdit', query: { id: row.case_id } })
}

const showReport = () => {
  state.showReportDialog = !state.showReportDialog
  nextTick(() => initReport())
}

defineExpose({
  showReport,
})
</script>

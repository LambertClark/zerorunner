<template>
  <div class="app-container">
    <!-- 报告统计 -->
    <el-card style="margin-bottom: 12px" v-if="state.statisticsData">
      <ReportStatistics :data="state.statisticsData"/>
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
            v-model="state.viewErrOnly"
            class="ml10"
            @change="viewErrOrFailApi"
        >
          只看失败/错误步骤
        </el-checkbox>
      </div>

      <z-table
          ref="tableRef"
          :columns="state.columns"
          :data="state.listData"
          :show-page="false"
          row-key="id"
      />
    </el-card>

    <!-- 步骤详情抽屉 -->
    <el-drawer
        v-model="state.showStepDetail"
        title="步骤详情"
        size="55%"
        direction="ltr"
        append-to-body
        destroy-on-close
    >
      <div style="padding: 16px" v-if="state.stepDetail">
        <el-descriptions :column="1" border size="small">
          <el-descriptions-item label="步骤名称">{{ state.stepDetail.name }}</el-descriptions-item>
          <el-descriptions-item label="操作类型">
            {{ operationTypeToZh[state.stepDetail.operation_type] || state.stepDetail.operation_type }}
          </el-descriptions-item>
          <el-descriptions-item label="模板步骤">{{ state.stepDetail.is_template ? '是' : '否' }}</el-descriptions-item>
          <el-descriptions-item label="执行状态">
            <el-tag :type="statusTagType(state.stepDetail.operation_state)">
              {{ state.stepDetail.operation_state || '-' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="错误类型">{{ state.stepDetail.error_type || '-' }}</el-descriptions-item>
          <el-descriptions-item label="耗时(s)">{{ state.stepDetail.duration ?? '-' }}</el-descriptions-item>
          <el-descriptions-item label="错误信息">{{ state.stepDetail.error_msg || '-' }}</el-descriptions-item>
        </el-descriptions>

        <!-- 截图对比 -->
        <el-row :gutter="12" style="margin-top: 16px">
          <el-col :span="12" v-if="state.stepDetail.original_image_path">
            <div class="image-label">原始素材</div>
            <el-image
                :src="state.stepDetail.original_image_path"
                fit="contain"
                style="width: 100%; max-height: 300px;"
                :preview-src-list="[state.stepDetail.original_image_path]"
                preview-teleported
            />
          </el-col>
          <el-col :span="12" v-if="state.stepDetail.state_image">
            <div class="image-label">执行截图</div>
            <el-image
                :src="state.stepDetail.state_image"
                fit="contain"
                style="width: 100%; max-height: 300px;"
                :preview-src-list="[state.stepDetail.state_image]"
                preview-teleported
            />
          </el-col>
        </el-row>

        <!-- 执行前截图 -->
        <div v-if="state.screenshotBeforeUrlList.length > 0" style="margin-top: 12px">
          <div class="image-label">执行前截图</div>
          <el-image
              v-for="(url, idx) in state.screenshotBeforeUrlList"
              :key="idx"
              :src="url"
              fit="contain"
              style="width: 100%; max-height: 200px; margin-bottom: 8px;"
              :preview-src-list="state.screenshotBeforeUrlList"
              preview-teleported
          />
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script setup name="pcReportDetail">
import { h, onMounted, reactive, ref } from 'vue'
import { ElButton, ElTag, ElImage } from 'element-plus'
import { useRouter, useRoute } from 'vue-router'
import { usePcReportApi } from '/@/api/usePcAutoApi/pcReport'
import useMouseData from '/@/hooks/pcAutoTest/useMouseData'
import ReportStatistics from '/@/components/Z-Report/ApiReport/components/ReportStatistics.vue'

const props = defineProps({
  reportId: {
    type: [Number, String, null],
    default: null,
  },
  reportInfo: {
    type: Object,
    default: null,
  },
  isDebug: {
    type: Boolean,
    default: false,
  },
})

const { operationTypeToZh } = useMouseData()

const route = useRoute()
const router = useRouter()
const tableRef = ref()

const state = reactive({
  listData: [],
  statisticsData: null,
  statQuery: {},
  screenshotUrlList: [],
  screenshotBeforeUrlList: [],
  showBeforePreview: false,
  showFullscreenPreview: false,
  showStepDetail: false,
  stepDetail: null,
  viewErrOnly: false,
  listQuery: {
    report_id: null,
    name: '',
    status_list: [],
    case_id: null,
    page: 1,
    pageSize: 200,
  },
  columns: [
    { label: 'N', columnType: 'index', align: 'center', width: 'auto' },
    {
      key: 'name', label: '步骤名称', width: '',
      render: ({ row }) => h(ElButton, {
        link: true, type: 'primary',
        onClick: () => viewStepDetail(row),
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
    {
      label: '操作', fixed: 'right', align: 'center', width: '80',
      render: ({ row }) => h(ElButton, {
        type: 'primary',
        onClick: () => viewStepDetail(row),
      }, () => '详情'),
    },
  ],
})

const statusTagType = (status) => {
  const map = { SUCCESS: 'success', FAILURE: 'danger', ERROR: 'danger', SKIP: 'info' }
  return map[status] || 'info'
}

const viewStepDetail = (row) => {
  state.stepDetail = row
  state.screenshotBeforeUrlList = row.before_images || []
  state.screenshotUrlList = row.state_image ? [row.state_image] : []
  state.showStepDetail = true
}

const initReport = () => {
  const id = props.reportId || route.query.id
  if (id) {
    state.listQuery.report_id = id
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
    state.screenshotBeforeUrlList = state.listData
      .filter((s) => s.original_image_path)
      .map((s) => s.original_image_path)
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
  usePcReportApi().getReportStatistics({ report_id: state.listQuery.report_id }).then((res) => {
    state.statisticsData = res.data
  })
}

onMounted(() => {
  initReport()
})
</script>

<style lang="scss" scoped>
.image-label {
  font-size: 12px;
  color: #909399;
  margin-bottom: 6px;
  text-align: center;
}
</style>

<template>
  <div class="app-container">
    <!-- 报告统计 -->
    <el-card style="margin-bottom: 12px">
      <PcReportStatistics :data="state.statistics" :report="state.report"/>
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
            @change="onErrFilterChange"
        >
          只看失败/错误步骤
        </el-checkbox>
      </div>

      <z-table
          ref="tableRef"
          :columns="state.columns"
          :data="state.listData"
          :show-page="false"
          :loading="state.tableLoading"
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
          <el-descriptions-item label="操作类型">{{ state.stepDetail.operation_type }}</el-descriptions-item>
          <el-descriptions-item label="执行状态">
            <el-tag :type="statusTagType(state.stepDetail.operation_state)">
              {{ state.stepDetail.operation_state || '-' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="耗时(s)">{{ state.stepDetail.duration ?? '-' }}</el-descriptions-item>
          <el-descriptions-item label="错误信息">{{ state.stepDetail.error_msg || '-' }}</el-descriptions-item>
        </el-descriptions>

        <!-- 截图对比 -->
        <el-row :gutter="12" style="margin-top: 16px">
          <el-col :span="12" v-if="state.stepDetail.original_image_path">
            <div class="image-label">原始素材</div>
            <el-image
                :src="getPicUrl(state.stepDetail.original_image_path)"
                fit="contain"
                style="width: 100%; max-height: 300px;"
                :preview-src-list="[getPicUrl(state.stepDetail.original_image_path)]"
                preview-teleported
            />
          </el-col>
          <el-col :span="12" v-if="state.stepDetail.state_image">
            <div class="image-label">执行截图</div>
            <el-image
                :src="getPicUrl(state.stepDetail.state_image)"
                fit="contain"
                style="width: 100%; max-height: 300px;"
                :preview-src-list="[getPicUrl(state.stepDetail.state_image)]"
                preview-teleported
            />
          </el-col>
        </el-row>
      </div>
    </el-drawer>
  </div>
</template>

<script setup name="pcReportDetail">
import { h, onMounted, reactive, ref } from 'vue'
import { ElButton, ElTag, ElImage } from 'element-plus'
import { useRoute } from 'vue-router'
import { usePcReportApi } from '/@/api/usePcAutoApi/pcReport.js'
import { getBaseApiUrl } from '/@/utils/config'
import PcReportStatistics from './pcReportStatistics.vue'

const route = useRoute()
const tableRef = ref()

const state = reactive({
  report: {},
  statistics: {},
  listData: [],
  tableLoading: false,
  viewErrOnly: false,
  listQuery: {
    report_id: null,
    name: '',
    status_list: [],
  },
  showStepDetail: false,
  stepDetail: null,
  columns: [
    { label: 'N', columnType: 'index', align: 'center', width: 'auto' },
    {
      key: 'name', label: '步骤名称', width: '',
      render: ({ row }) => h(ElButton, {
        link: true, type: 'primary',
        onClick: () => viewDetail(row),
      }, () => row.name),
    },
    { key: 'operation_type', label: '操作类型', align: 'center', width: '160' },
    { key: 'duration', label: '耗时(s)', align: 'center', width: '100' },
    {
      key: 'operation_state', label: '状态', align: 'center', width: '100',
      render: ({ row }) => h(ElTag, {
        type: statusTagType(row.operation_state),
      }, () => row.operation_state || '-'),
    },
    {
      key: 'state_image', label: '执行截图', align: 'center', width: '120',
      render: ({ row }) => row.state_image
        ? h(ElImage, {
            src: getPicUrl(row.state_image),
            fit: 'contain',
            previewSrcList: [getPicUrl(row.state_image)],
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
        onClick: () => viewDetail(row),
      }, () => '详情'),
    },
  ],
})

const getPicUrl = (url) => {
  if (!url) return ''
  return url.startsWith('http') ? url : `${getBaseApiUrl()}/${url}`
}

const statusTagType = (status) => {
  const map = { SUCCESS: 'success', FAILURE: 'danger', ERROR: 'danger', SKIP: 'info' }
  return map[status] || 'info'
}

const getReportInfo = () => {
  usePcReportApi().getReportInfo({ id: route.query.id }).then((res) => {
    state.report = res.data
    state.statistics = res.data.statistics || {}
    state.listData = res.data.step_results || []
  })
}

const searchDetail = () => {
  getReportInfo()
}

const onErrFilterChange = (val) => {
  if (val) {
    state.listData = (state.report.step_results || []).filter(
      (s) => ['FAILURE', 'ERROR'].includes(s.operation_state)
    )
  } else {
    state.listData = state.report.step_results || []
  }
}

const viewDetail = (row) => {
  state.stepDetail = row
  state.showStepDetail = true
}

onMounted(() => {
  if (route.query.id) {
    getReportInfo()
  }
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

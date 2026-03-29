<template>
  <div class="report-statistics">
    <el-row :gutter="20">
      <el-col :span="8">
        <div class="chart-title">总耗时</div>
        <div ref="requestTime" class="chart-box"></div>
      </el-col>
      <el-col :span="8">
        <div class="chart-title">用例通过率</div>
        <div ref="apiTestCase" class="chart-box"></div>
      </el-col>
      <el-col :span="8">
        <div class="chart-title">步骤通过率</div>
        <div ref="apiTestStep" class="chart-box"></div>
      </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 16px" v-if="start_time || exec_user_name">
      <el-col :span="12">
        <div class="stat-meta">开始时间：{{ start_time || '-' }}</div>
      </el-col>
      <el-col :span="12">
        <div class="stat-meta">执行人：{{ exec_user_name || '-' }}</div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup name="ReportStatistics">
import * as echarts from 'echarts'
import { nextTick, onMounted, onUnmounted, reactive, ref, watch } from 'vue'

const props = defineProps({
  data: {
    type: Object,
    default: () => ({}),
  },
  start_time: {
    type: String,
    default: '',
  },
  exec_user_name: {
    type: String,
    default: '',
  },
})

const requestTime = ref()
const apiTestCase = ref()
const apiTestStep = ref()

const state = reactive({
  requestTimeECharts: null,
  caseECharts: null,
  stepECharts: null,
})

const getOption = (value) => {
  return {
    graphic: {
      elements: [
        {
          type: 'text',
          left: 'center',
          top: 'center',
          style: {
            text: `${value}%`,
            textAlign: 'center',
            fill: '#303133',
            fontSize: 18,
            fontWeight: 'bold',
          },
        },
      ],
    },
    series: [
      {
        type: 'pie',
        radius: ['55%', '75%'],
        avoidLabelOverlap: false,
        label: { show: false },
        data: [
          { value: 100 - value, itemStyle: { color: '#e6e6e6' } },
          { value: value, itemStyle: { color: '#409eff' } },
        ],
      },
    ],
  }
}

const initRequestTime = () => {
  state.requestTimeECharts = echarts.init(requestTime.value)
  state.requestTimeECharts.setOption(getOption(100))
}

const initApiTestCase = () => {
  const value = props.data?.case_pass_rate ?? 0
  state.caseECharts = echarts.init(apiTestCase.value)
  state.caseECharts.setOption(getOption(value))
}

const initApiTestStep = () => {
  const value = props.data?.step_pass_rate ?? 0
  state.stepECharts = echarts.init(apiTestStep.value)
  state.stepECharts.setOption(getOption(value))
}

const initEcharts = () => {
  initRequestTime()
  initApiTestCase()
  initApiTestStep()
}

onMounted(() => {
  nextTick(() => {
    initEcharts()
    watch(
      () => props.data,
      () => {
        initApiTestCase()
        initApiTestStep()
      },
      { deep: true }
    )
  })

  window.onresize = () => {
    state.requestTimeECharts?.resize()
    state.caseECharts?.resize()
    state.stepECharts?.resize()
  }
})

onUnmounted(() => {
  state.requestTimeECharts?.dispose()
  state.caseECharts?.dispose()
  state.stepECharts?.dispose()
})
</script>

<style lang="scss" scoped>
.report-statistics {
  .chart-title {
    text-align: center;
    font-size: 14px;
    color: #606266;
    margin-bottom: 6px;
  }

  .chart-box {
    height: 200px;
  }

  .stat-meta {
    font-size: 13px;
    color: #909399;
    text-align: center;
  }
}
</style>

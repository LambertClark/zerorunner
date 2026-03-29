<template>
  <div class="app-container">
    <!-- 统计卡片 -->
    <el-row :gutter="16" style="margin-bottom: 16px">
      <el-col :span="6" v-for="item in deviceStats" :key="item.label">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-value" :style="{ color: item.color }">{{ item.value }}</div>
            <div class="stat-label">{{ item.label }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="16">
      <el-col :span="12">
        <el-card>
          <template #header>设备类型分布</template>
          <div ref="typeChartRef" style="height: 280px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>近7日在线趋势</template>
          <div ref="trendChartRef" style="height: 280px"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最近设备列表 -->
    <el-card style="margin-top: 16px">
      <template #header>最近活跃设备</template>
      <el-table :data="recentDevices" border>
        <el-table-column prop="name" label="设备名称"/>
        <el-table-column prop="ip" label="IP地址" width="160"/>
        <el-table-column prop="lastActive" label="最近活跃" width="180"/>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === 'online' ? 'success' : 'info'">
              {{ row.status === 'online' ? '在线' : '离线' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160" align="center">
          <template #default="{ row }">
            <el-button type="primary" link @click="viewDevice(row)">查看</el-button>
            <el-button type="success" link @click="connectDevice(row)">连接</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'

const router = useRouter()

const typeChartRef = ref()
const trendChartRef = ref()

const deviceStats = ref([
  { label: '设备总数', value: 12, color: '#409eff' },
  { label: '在线设备', value: 8, color: '#67c23a' },
  { label: '离线设备', value: 4, color: '#f56c6c' },
  { label: '今日执行', value: 35, color: '#e6a23c' },
])

const recentDevices = ref([
  { id: 1, name: '测试机-001', ip: '192.168.1.101', lastActive: '2026-03-30 10:22', status: 'online' },
  { id: 2, name: '测试机-002', ip: '192.168.1.102', lastActive: '2026-03-30 09:15', status: 'offline' },
  { id: 3, name: '测试机-003', ip: '192.168.1.103', lastActive: '2026-03-30 11:05', status: 'online' },
])

const viewDevice = (row) => {
  router.push({ path: `/pcAutoTest/deviceList/${row.id}` })
}

const connectDevice = (row) => {
  router.push({ path: `/pcAutoTest/deviceList/${row.id}` })
}

const initTypeChart = () => {
  const chart = echarts.init(typeChartRef.value)
  chart.setOption({
    tooltip: { trigger: 'item' },
    series: [
      {
        type: 'pie',
        radius: '60%',
        data: [
          { name: 'Windows', value: 8 },
          { name: 'macOS', value: 3 },
          { name: 'Linux', value: 1 },
        ],
      },
    ],
  })
}

const initTrendChart = () => {
  const chart = echarts.init(trendChartRef.value)
  chart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: ['03-24', '03-25', '03-26', '03-27', '03-28', '03-29', '03-30'],
    },
    yAxis: { type: 'value' },
    series: [
      {
        name: '在线数',
        type: 'line',
        smooth: true,
        data: [6, 7, 5, 8, 9, 7, 8],
      },
    ],
  })
}

onMounted(() => {
  initTypeChart()
  initTrendChart()
})
</script>

<style lang="scss" scoped>
.stat-card {
  text-align: center;

  .stat-value {
    font-size: 28px;
    font-weight: bold;
  }

  .stat-label {
    font-size: 13px;
    color: #909399;
    margin-top: 4px;
  }
}
</style>

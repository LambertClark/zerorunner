<template>
  <el-row :gutter="20">
    <el-col :span="6">
      <div class="stat-item">
        <div class="stat-label">运行结果</div>
        <el-tag :type="report.success ? 'success' : 'danger'" size="large">
          {{ report.success ? '通过' : '不通过' }}
        </el-tag>
      </div>
    </el-col>
    <el-col :span="6">
      <div class="stat-item">
        <div class="stat-label">步骤总数</div>
        <div class="stat-value">{{ data.step_count ?? report.step_count ?? '-' }}</div>
      </div>
    </el-col>
    <el-col :span="6">
      <div class="stat-item">
        <div class="stat-label">成功 / 失败</div>
        <div class="stat-value">
          <span style="color: #67c23a">{{ data.success_count ?? report.success_count ?? '-' }}</span>
          /
          <span style="color: #f56c6c">{{ data.failure_count ?? report.failure_count ?? '-' }}</span>
        </div>
      </div>
    </el-col>
    <el-col :span="6">
      <div class="stat-item">
        <div class="stat-label">执行耗时(s)</div>
        <div class="stat-value">{{ report.duration ?? '-' }}</div>
      </div>
    </el-col>
    <el-col :span="6" style="margin-top: 12px">
      <div class="stat-item">
        <div class="stat-label">开始时间</div>
        <div class="stat-value" style="font-size: 13px">{{ report.start_time ?? '-' }}</div>
      </div>
    </el-col>
    <el-col :span="6" style="margin-top: 12px">
      <div class="stat-item">
        <div class="stat-label">执行人</div>
        <div class="stat-value">{{ report.exec_user_name ?? '-' }}</div>
      </div>
    </el-col>
    <el-col :span="12" style="margin-top: 12px" v-if="report.error_msg">
      <div class="stat-item">
        <div class="stat-label">错误信息</div>
        <el-text type="danger">{{ report.error_msg }}</el-text>
      </div>
    </el-col>
  </el-row>
</template>

<script setup name="PcReportStatistics">
defineProps({
  data: {
    type: Object,
    default: () => ({}),
  },
  report: {
    type: Object,
    default: () => ({}),
  },
})
</script>

<style lang="scss" scoped>
.stat-item {
  text-align: center;

  .stat-label {
    font-size: 12px;
    color: #909399;
    margin-bottom: 6px;
  }

  .stat-value {
    font-size: 20px;
    font-weight: 600;
    color: #303133;
  }
}
</style>

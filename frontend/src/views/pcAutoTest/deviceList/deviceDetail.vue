<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div style="display: flex; align-items: center; justify-content: space-between">
          <span>设备详情</span>
          <div>
            <el-button type="primary" :icon="Connection" @click="connectDevice">连接设备</el-button>
            <el-button type="success" :icon="VideoPlay" @click="runTest">运行测试</el-button>
            <el-button :icon="Document" @click="viewLogs">查看日志</el-button>
            <el-button :icon="Camera" @click="takeScreenshot">截图</el-button>
            <el-button type="warning" :icon="Refresh" @click="restartDevice">重启</el-button>
            <el-button :icon="Edit" @click="editDevice">编辑</el-button>
          </div>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="设备ID">{{ deviceInfo.id }}</el-descriptions-item>
        <el-descriptions-item label="设备名称">{{ deviceInfo.name }}</el-descriptions-item>
        <el-descriptions-item label="IP地址">{{ deviceInfo.ip }}</el-descriptions-item>
        <el-descriptions-item label="操作系统">{{ deviceInfo.os }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="deviceInfo.status === 'online' ? 'success' : 'danger'">
            {{ deviceInfo.status === 'online' ? '在线' : '离线' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="最近活跃">{{ deviceInfo.lastActive }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ deviceInfo.remark || '-' }}</el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Connection,
  VideoPlay,
  Document,
  Camera,
  Refresh,
  Edit,
} from '@element-plus/icons-vue'

const route = useRoute()

const deviceInfo = ref({
  id: '',
  name: '',
  ip: '',
  os: 'Windows',
  status: 'online',
  lastActive: '',
  remark: '',
})

const connectDevice = () => {
  ElMessage.success(`正在连接设备 ${deviceInfo.value.name}`)
}

const runTest = () => {
  ElMessage.info('运行测试功能开发中')
}

const viewLogs = () => {
  ElMessage.info('查看日志功能开发中')
}

const takeScreenshot = () => {
  ElMessage.info('截图功能开发中')
}

const restartDevice = () => {
  ElMessageBox.confirm('确定重启该设备吗？', '提示', { type: 'warning' }).then(() => {
    ElMessage.success('重启指令已发送')
  })
}

const editDevice = () => {
  ElMessage.info('编辑功能开发中')
}

onMounted(() => {
  const id = route.params.id
  // 模拟加载设备详情
  deviceInfo.value = {
    id,
    name: `测试机-${String(id).padStart(3, '0')}`,
    ip: `192.168.1.${100 + Number(id)}`,
    os: 'Windows',
    status: 'online',
    lastActive: '2026-03-30 11:00',
    remark: '',
  }
})
</script>

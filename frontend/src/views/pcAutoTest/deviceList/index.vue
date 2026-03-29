<template>
  <div class="app-container">
    <!-- 设备类型切换 -->
    <el-card style="margin-bottom: 16px">
      <el-radio-group v-model="activeDeviceType" @change="handleDeviceTypeSelect">
        <el-radio-button
            v-for="(label, type) in deviceTypeMap"
            :key="type"
            :label="type"
        >
          <el-icon style="margin-right: 4px">
            <Monitor v-if="type === 'windows'"/>
            <Apple v-else-if="type === 'mac'"/>
            <Platform v-else/>
          </el-icon>
          {{ label }}
        </el-radio-button>
      </el-radio-group>
    </el-card>

    <!-- 设备列表 -->
    <el-card>
      <div class="mb15">
        <el-button type="primary" :icon="Plus" @click="addDevice">新增设备</el-button>
      </div>
      <el-table :data="deviceList" border style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" align="center"/>
        <el-table-column prop="name" label="设备名称"/>
        <el-table-column prop="ip" label="IP地址" width="160"/>
        <el-table-column prop="os" label="操作系统" width="120" align="center"/>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === 'online' ? 'success' : 'danger'">
              {{ row.status === 'online' ? '在线' : '离线' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="viewDeviceDetail(row)">详情</el-button>
            <el-button type="warning" link @click="editDevice(row)">编辑</el-button>
            <el-button type="danger" link @click="deleteDevice(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { Monitor, Apple, Platform, Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()

const activeDeviceType = ref('windows')
const currentDeviceType = ref('windows')

const deviceTypeMap = {
  windows: 'Windows',
  mac: 'macOS',
  linux: 'Linux',
}

const deviceList = ref([
  { id: 1, name: '测试机-001', ip: '192.168.1.101', os: 'Windows', status: 'online' },
  { id: 2, name: '测试机-002', ip: '192.168.1.102', os: 'Windows', status: 'offline' },
  { id: 3, name: '测试机-003', ip: '192.168.1.103', os: 'macOS', status: 'online' },
])

const handleDeviceTypeSelect = (type) => {
  currentDeviceType.value = type
  loadDeviceList()
}

const loadDeviceList = () => {
  // 模拟数据加载
}

const addDevice = () => {
  ElMessage.info('新增设备功能开发中')
}

const viewDeviceDetail = (row) => {
  router.push({ path: `/pcAutoTest/deviceList/${row.id}` })
}

const editDevice = (row) => {
  ElMessage.info(`编辑设备：${row.name}`)
}

const deleteDevice = (row) => {
  ElMessageBox.confirm(`确定删除设备 "${row.name}" 吗？`, '提示', {
    type: 'warning',
  }).then(() => {
    const idx = deviceList.value.findIndex((d) => d.id === row.id)
    if (idx !== -1) deviceList.value.splice(idx, 1)
    ElMessage.success('删除成功')
  })
}
</script>

<template>
  <div class="app-container">
    <el-card>
      <div class="mb15">
        <el-button type="primary" @click="search">查询</el-button>
        <el-button type="success" @click="openDialog">新增执行机</el-button>
      </div>

      <z-table
          ref="tableRef"
          :columns="state.columns"
          :data="state.listData"
          v-model:page-size="state.listQuery.pageSize"
          v-model:page="state.listQuery.page"
          :total="state.total"
          @pagination-change="getDevices"
      />
    </el-card>
  </div>
</template>

<script setup name="pcAgentDeviceList">
import { h, onMounted, onUnmounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElTag } from 'element-plus'
import { usePcDevicesApi } from '/@/api/usePcAutoApi/pcDevices.js'
// TODO: 创建 useAppAutoTestApi 后取消注释
// import { useAppAutoTestApi } from '/@/api/usePcAutoApi/appAutoTest.js'

const router = useRouter()
const tableRef = ref()
let timer = null

/**
 * collection_time 距今超过 60 秒视为离线
 */
const calculateStatus = (collectionTime) => {
  if (!collectionTime) return 'offline'
  const diff = Date.now() - new Date(collectionTime).getTime()
  return diff <= 60 * 1000 ? 'online' : 'offline'
}

const state = reactive({
  listData: [],
  total: 0,
  listQuery: { page: 1, pageSize: 20 },
  dialogVisible: false,
  editRow: null,
  columns: [
    { label: '序号', columnType: 'index', align: 'center', width: 'auto' },
    { key: 'user_name', label: '用户名', align: 'center', width: '120' },
    { key: 'identity', label: '执行机标识', align: 'center', width: '180' },
    { key: 'os_name', label: '操作系统', align: 'center', width: '140' },
    { key: 'screen_size', label: '显示器尺寸', align: 'center', width: '120' },
    { key: 'memory', label: '内存', align: 'center', width: '100' },
    { key: 'cpu', label: 'CPU', align: 'center', width: '120' },
    { key: 'disk', label: '磁盘', align: 'center', width: '120' },
    {
      key: 'collection_time',
      label: '状态',
      align: 'center',
      width: '90',
      render: ({ row }) => {
        const status = calculateStatus(row.collection_time)
        return h(ElTag, { type: status === 'online' ? 'success' : 'danger' }, () => status === 'online' ? '在线' : '离线')
      },
    },
    { key: 'updation_date', label: '更新时间', align: 'center', width: '160' },
    {
      label: '操作',
      align: 'center',
      width: '160',
      render: ({ row }) => [
        h('el-button', {
          size: 'small',
          type: 'primary',
          onClick: () => editDevice(row),
        }, '编辑'),
        h('el-button', {
          size: 'small',
          type: row.status === 'online' ? 'danger' : 'success',
          onClick: () => changeDeviceStatus(row),
        }, row.status === 'online' ? '禁用' : '启用'),
      ],
    },
  ],
})

const getDevices = () => {
  if (tableRef.value) tableRef.value.openLoading?.()
  usePcDevicesApi().getPcDevices(state.listQuery)
    .then((res) => {
      state.listData = res.data.rows
      state.total = res.data.rowTotal
    })
    .finally(() => {
      if (tableRef.value) tableRef.value.closeLoading?.()
    })
}

const search = () => {
  state.listQuery.page = 1
  getDevices()
}

const openDialog = () => {
  state.editRow = null
  state.dialogVisible = true
}

const toggleDialog = (visible) => {
  state.dialogVisible = visible !== undefined ? visible : !state.dialogVisible
}

const editDevice = (row) => {
  state.editRow = row
  state.dialogVisible = true
}

const changeDeviceStatus = (row) => {
  // 切换设备启用/禁用状态
  usePcDevicesApi().getPcDevices({ id: row.id, status: row.status === 'online' ? 'offline' : 'online' })
    .then(() => {
      getDevices()
    })
}

onMounted(() => {
  getDevices()
  timer = setInterval(getDevices, 60000)
})

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
})
</script>

<style lang="scss" scoped></style>

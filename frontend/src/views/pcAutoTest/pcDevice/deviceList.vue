<template>
  <div class="app-container">
    <el-card>
      <div class="mb15">
        <el-button type="primary" @click="getList">刷新</el-button>
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
  </div>
</template>

<script setup name="pcDeviceList">
import { h, onMounted, reactive, ref } from 'vue'
import { ElTag } from 'element-plus'
import { usePcDevicesApi } from '/@/api/usePcAutoApi/pcDevices.js'

const tableRef = ref()
const devicesApi = usePcDevicesApi()

const state = reactive({
  listData: [],
  total: 0,
  listQuery: { page: 1, pageSize: 20 },
  columns: [
    { label: '序号', columnType: 'index', align: 'center', width: 'auto' },
    { key: 'name', label: '执行机名称', width: '' },
    { key: 'host', label: '主机地址', align: 'center', width: '160' },
    { key: 'port', label: '端口', align: 'center', width: '80' },
    {
      key: 'status', label: '状态', align: 'center', width: '100',
      render: ({ row }) => h(ElTag, {
        type: row.status === 'online' ? 'success' : 'danger',
      }, () => row.status === 'online' ? '在线' : '离线'),
    },
    { key: 'os_info', label: '系统信息', align: 'center', width: '180' },
    { key: 'last_heartbeat', label: '最后心跳', align: 'center', width: '160' },
    { key: 'remarks', label: '备注', width: '' },
  ],
})

const getList = () => {
  tableRef.value.openLoading()
  devicesApi.getList(state.listQuery)
    .then((res) => {
      state.listData = res.data.rows
      state.total = res.data.rowTotal
    })
    .finally(() => tableRef.value.closeLoading())
}

onMounted(() => { getList() })
</script>

<style lang="scss" scoped></style>

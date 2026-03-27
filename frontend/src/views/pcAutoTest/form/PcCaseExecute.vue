<template>
  <el-dialog
      v-model="dialogVisible"
      title="选择执行机并运行"
      width="560px"
      append-to-body
      :close-on-click-modal="false"
      destroy-on-close
  >
    <el-form label-width="90px" size="small">
      <el-form-item label="执行机">
        <el-select
            v-model="state.deviceId"
            placeholder="请选择在线执行机"
            filterable
            style="width: 100%"
        >
          <el-option
              v-for="device in state.deviceList"
              :key="device.id"
              :label="`${device.name}（${device.host || device.ip || ''}）`"
              :value="device.id"
          />
        </el-select>
        <el-button size="small" type="primary" link style="margin-top: 4px" @click="fetchDevices">
          刷新设备列表
        </el-button>
      </el-form-item>
    </el-form>

    <el-empty v-if="state.deviceList.length === 0 && !state.loading" description="暂无在线执行机，请先启动 PC Agent"/>

    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button
          type="primary"
          :loading="state.running"
          :disabled="!state.deviceId"
          @click="runCases"
      >
        运行
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup name="PcCaseExecute">
import { computed, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { usePcDevicesApi } from '/@/api/usePcAutoApi/pcDevices.js'
import { usePcTestCaseApi } from '/@/api/usePcAutoApi/pcTestCase.js'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false,
  },
  // 要执行的用例 id 数组
  caseIds: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['update:visible', 'run-success'])

const router = useRouter()

const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => emit('update:visible', val),
})

const state = reactive({
  deviceList: [],
  deviceId: null,
  loading: false,
  running: false,
})

const fetchDevices = () => {
  state.loading = true
  usePcDevicesApi().getOnlineList({}).then((res) => {
    state.deviceList = res.data || []
    if (state.deviceList.length > 0 && !state.deviceId) {
      state.deviceId = state.deviceList[0].id
    }
  }).finally(() => {
    state.loading = false
  })
}

const runCases = () => {
  if (!state.deviceId) {
    ElMessage.warning('请先选择执行机')
    return
  }
  state.running = true
  usePcTestCaseApi().runCases({
    case_ids: props.caseIds,
    device_id: state.deviceId,
  }).then((res) => {
    ElMessage.success('执行成功，正在跳转报告...')
    const reportId = res.data?.report_id || res.data?.id
    emit('run-success', reportId)
    dialogVisible.value = false
    if (reportId) {
      router.push({ name: 'pcReportDetail', query: { id: reportId } })
    }
  }).finally(() => {
    state.running = false
  })
}

onMounted(() => {
  fetchDevices()
})
</script>

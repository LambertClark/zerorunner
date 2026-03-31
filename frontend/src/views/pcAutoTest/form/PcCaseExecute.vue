<template>
  <el-dialog
      v-model="state.isShowDialog"
      title="选择执行机并运行"
      width="560px"
      append-to-body
      :close-on-click-modal="false"
      destroy-on-close
  >
    <el-form label-width="100px" size="small">
      <el-form-item label="用例">
        <span>{{ state.case_title }}</span>
      </el-form-item>

      <el-form-item label="执行机">
        <el-select
            v-model="state.device_identity"
            placeholder="请选择在线执行机"
            filterable
            style="width: 100%"
        >
          <el-option
              v-for="device in state.deviceList"
              :key="device.identity"
              :label="`${device.name || device.identity}（${device.host || device.ip || ''}）`"
              :value="device.identity"
          />
        </el-select>
        <el-button size="small" type="primary" link style="margin-top: 4px" @click="getDevices">
          刷新设备列表
        </el-button>
      </el-form-item>
    </el-form>

    <el-empty
        v-if="state.deviceList.length === 0"
        description="暂无在线执行机（5分钟内），请先启动 PC Agent"
    />

    <template #footer>
      <el-button @click="onCancel">取消</el-button>
      <el-button
          type="primary"
          :disabled="!state.device_identity"
          @click="run"
      >
        运行
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup name="PcCaseExecute">
import { reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserApi } from '/@/api/useSystemApi/user'
import { usePcDevicesApi } from '/@/api/usePcAutoApi/pcDevices'
import { usePcTestCaseApi } from '/@/api/usePcAutoApi/pcTestCase'

const emit = defineEmits(['open-report'])

const state = reactive({
  isShowDialog: false,
  case_id: null,
  device_identity: '',
  plan_id: null,
  plan_name: '',
  case_title: '',
  created_by_name: '',
  deviceList: [],
  current_user: null,
  filtersQuery: {
    app_platform: '',
    agent_id: '',
  },
})

const openDialog = (row) => {
  state.case_id = row?.id ?? null
  state.case_title = row?.title ?? row?.name ?? ''
  state.plan_id = row?.plan_id ?? null
  state.plan_name = row?.plan_name ?? ''
  state.created_by_name = row?.created_by_name ?? ''
  state.device_identity = ''
  state.isShowDialog = true
  getDevices()
  getCurrentUser()
}

const closeDialog = () => {
  state.isShowDialog = false
}

const onCancel = () => {
  closeDialog()
}

const getDevices = () => {
  const params = {
    app_platform: state.filtersQuery.app_platform,
    agent_id: state.filtersQuery.agent_id,
    status: 1,
    recent_minutes: 5,
  }
  usePcDevicesApi().getPcDevices(params).then((res) => {
    const rows = res.data?.rows || res.data || []
    state.deviceList = rows.map((d) => ({ ...d, status: 'online' }))
    if (state.deviceList.length > 0 && !state.device_identity) {
      state.device_identity = state.deviceList[0].identity
    }
  })
}

const getCurrentUser = () => {
  useUserApi().getUserInfoByToken().then((res) => {
    state.current_user = res.data
  }).catch(() => {})
}

const run = () => {
  runPcTestCases()
}

const runPcTestCases = () => {
  if (!state.device_identity) {
    ElMessage.warning('请先选择执行机')
    return
  }
  usePcTestCaseApi().runPcCases({
    case_id: state.case_id,
    pc_device_identity: state.device_identity,
  }).then((res) => {
    const reportId = res.data?.report_id
    if (!reportId) {
      ElMessage.warning('执行请求已发出，但未返回报告ID，请稍后在报告列表查看结果')
      closeDialog()
      return
    }
    ElMessage.success('执行成功')
    closeDialog()
    emit('open-report', reportId)
  }).catch((err) => {
    const msg = err?.response?.data?.msg || err?.message || '执行失败，请检查执行机是否在线'
    ElMessage.error(msg)
  })
}

defineExpose({ openDialog })
</script>

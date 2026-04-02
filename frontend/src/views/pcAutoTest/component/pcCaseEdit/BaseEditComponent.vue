<template>
  <div class="app-container h100">
    <el-card class="step-content" style="height: 100%;" :body-style="{ height: 'calc(100% - 66.5px)' }">
      <template #header>
        <z-detail-page-header style="margin: 5px 0;" @back="goBack">
          <template #content>
            <span style="padding-right: 10px;">
              {{ state.editType === 'save' ? '新增' : '编辑' }}{{ pageTitle }}
            </span>
          </template>

          <template #extra>
            <!-- 左侧步骤面板下拉 -->
            <el-dropdown :hide-on-click="false" class="pr12">
              <el-button type="warning">
                添加步骤
                <el-icon class="el-icon--right"><ArrowDown/></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <template v-for="group in props.leftComponents" :key="group.label">
                    <el-dropdown-item disabled style="font-size: 12px; color: #909399;">
                      ── {{ group.label }} ──
                    </el-dropdown-item>
                    <el-dropdown-item
                        v-for="item in group.items"
                        :key="item.step_type"
                        :style="{ color: getStepTypeInfo(item.step_type, 'color') }"
                        @click="handleAddData(item.step_type)"
                    >
                      <component
                          v-if="getStepTypeInfo(item.step_type, 'icon')"
                          :is="getStepTypeInfo(item.step_type, 'icon')"
                          style="padding: 0 5px; font-size: 16px"
                          :style="{ color: getStepTypeInfo(item.step_type, 'color') }"
                      />
                      {{ item.label }}
                    </el-dropdown-item>
                  </template>
                </el-dropdown-menu>
              </template>
            </el-dropdown>

            <el-button type="success" @click="openRunPage">调试/执行</el-button>
            <el-button type="primary" @click="saveOrUpdate">保存</el-button>
          </template>
        </z-detail-page-header>
      </template>

      <z-splitpanes class="default-theme h100">
        <!-- 左侧表单 -->
        <z-pane :size="25">
          <div style="padding: 0 10px 0 0; overflow-y: auto; height: 100%;">
            <el-form
                ref="formRef"
                :model="state.form"
                :rules="state.rules"
                label-position="right"
                label-width="auto"
                size="small"
            >
              <el-form-item label="用例名称：" prop="name">
                <el-input v-model="state.form.name" placeholder="用例名称" clearable/>
              </el-form-item>

              <el-form-item label="所属项目：" prop="project_id">
                <el-select
                    v-model="state.form.project_id"
                    placeholder="选择所属项目"
                    filterable
                    style="width: 100%"
                >
                  <el-option
                      v-for="project in state.projectList"
                      :key="project.id"
                      :label="project.name"
                      :value="project.id"
                  />
                </el-select>
              </el-form-item>

              <el-form-item label="备注：" prop="remarks">
                <el-input v-model="state.form.remarks" placeholder="备注" clearable/>
              </el-form-item>

              <el-form-item label="用例变量：">
                <template #label>
                  <el-link type="primary" @click="state.activeTabName = 'variable'; state.showVariableDialog = true">
                    用例变量：
                  </el-link>
                </template>
                <el-link type="info" @click="state.showVariableDialog = true">
                  {{ getDataLength('headers') + getDataLength('variables') }}
                </el-link>
              </el-form-item>

              <el-form-item label="用例分类：" prop="case_category">
                <el-select
                    v-model="state.form.case_category"
                    placeholder="选择用例分类"
                    style="width: 100%"
                >
                  <el-option
                      v-for="opt in caseCategoryOptions"
                      :key="opt.value"
                      :label="opt.label"
                      :value="opt.value"
                  />
                </el-select>
              </el-form-item>

              <el-form-item label="步骤总数：">
                <span>{{ state.form.step_data?.length ?? 0 }}</span>
              </el-form-item>
            </el-form>
          </div>
        </z-pane>

        <!-- 右侧步骤树 -->
        <z-pane :size="75" :min-size="50">
          <PcAutoTestStepController
              ref="stepControllerRef"
              v-model:steps="state.form.step_data"
              :case_id="state.form.id"
              :use_type="'case'"
              style="margin-bottom: 10px"
              @step-deleted="handleStepDeleted"
          />
        </z-pane>
      </z-splitpanes>
    </el-card>

    <!-- 变量/请求头弹窗 -->
    <el-dialog
        draggable
        title="用例变量"
        v-model="state.showVariableDialog"
        width="769px"
        destroy-on-close
    >
      <el-tabs v-model="state.activeTabName">
        <el-tab-pane label="变量" name="variable">
          <template #label>
            <strong>变量</strong>
            <span class="ui-badge-circle" v-show="getDataLength('variables')">{{ getDataLength('variables') }}</span>
          </template>
          <VariableController :data="state.form.variables"/>
        </el-tab-pane>
        <el-tab-pane label="请求头" name="headers">
          <template #label>
            <strong>请求头</strong>
            <span class="ui-badge-circle" v-show="getDataLength('headers')">{{ getDataLength('headers') }}</span>
          </template>
          <HeadersController v-model:data="state.form.headers"/>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>

    <!-- 报告详情弹窗 -->
    <el-dialog
        draggable
        v-if="state.showReportDialog"
        v-model="state.showReportDialog"
        width="90%"
        top="5vh"
        destroy-on-close
        :close-on-click-modal="false"
    >
      <template #header><strong>报告详情</strong></template>
      <ReportDetail :report-info="state.reportInfo" :is-debug="true"/>
    </el-dialog>

    <!-- PC 执行弹窗 -->
    <PcCaseExecute ref="openRunConfigDialogRef" @open-report="openReport"/>
  </div>
</template>

<script setup name="BaseEditComponent">
import { onActivated, onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'
import { ArrowDown } from '@element-plus/icons-vue'
import 'splitpanes/dist/splitpanes.css'
import PcAutoTestStepController from '/@/components/PcAutoTestStepController/index.vue'
import VariableController from '/@/components/Z-StepController/variable/VariableController.vue'
import HeadersController from '/@/components/Z-StepController/headers/HeadersController.vue'
import ReportDetail from '/@/components/Z-Report/ApiReport/ReportInfo/ReportDetail.vue'
import PcCaseExecute from '/@/views/pcAutoTest/form/PcCaseExecute.vue'
import { useApiCaseApi } from '/@/api/useAutoApi/apiCase'
import { useEnvApi } from '/@/api/useAutoApi/env'
import { useProjectApi } from '/@/api/useAutoApi/project'
import { handleEmpty } from '/@/utils/other'
import { getStepTypeInfo, getStepTypesByUse } from '/@/utils/case'

const caseCategoryOptions = [
  { value: 'release', label: '发版用例' },
  { value: 'sit', label: 'SIT用例' },
  { value: 'performance', label: '性能用例' },
]

const props = defineProps({
  pageTitle: {
    type: String,
    default: 'PC 用例',
  },
  createFormData: {
    type: Function,
    required: true,
  },
  saveApi: {
    type: Function,
    required: true,
  },
  getCaseInfoApi: {
    type: Function,
    required: true,
  },
  leftComponents: {
    type: Array,
    default: () => [],
  },
})

const formRef = ref()
const stepControllerRef = ref()
const openRunConfigDialogRef = ref()
const route = useRoute()
const router = useRouter()

const state = reactive({
  editType: 'save',
  form: props.createFormData(),
  rules: {
    name: [{ required: true, message: '请输入用例名称', trigger: 'blur' }],
    project_id: [{ required: true, message: '请选择所属项目', trigger: 'blur' }],
    case_category: [{ required: true, message: '请选择用例分类', trigger: 'change' }],
  },
  projectList: [],
  envList: [],
  activeTabName: 'variable',
  showVariableDialog: false,
  showReportDialog: false,
  reportInfo: null,
  showRunPage: false,
  optTypes: getStepTypesByUse('case'),
  timestamp: null,
})

// 用于调试日志的元素标记
const logElement = (el) => {
  console.log('[BaseEditComponent] element:', el)
}

const initData = async () => {
  if (route.query.id) {
    state.editType = 'update'
    const { data } = await props.getCaseInfoApi({ id: route.query.id })
    state.form = data
    if (!state.form.step_data) state.form.step_data = []
    if (!state.form.variables) state.form.variables = []
    if (!state.form.headers) state.form.headers = []
    handleStepData(state.form.step_data || [])
  } else {
    state.editType = route.query.editType || 'save'
    state.form = props.createFormData()
  }
}

const handleStepData = (step_data) => {
  step_data.forEach((e) => {
    if (e.children_step) {
      handleStepData(e.children_step)
    } else {
      e.children_step = []
    }
  })
}

// pip_drag -> pip_slider_drag 归一化
const normalizePipDragStepType = (steps) => {
  steps.forEach((step) => {
    if (step.step_type === 'pip_drag') {
      step.step_type = 'pip_slider_drag'
    }
    if (step.request) {
      if (step.request.request_type_ === 'pip_drag') {
        step.request.request_type_ = 'pip_slider_drag'
      }
      if (step.request.comparator === 'PIP_DRAG') {
        step.request.comparator = 'PIP_SLIDER_DRAG'
      }
    }
    if (step.children_step && step.children_step.length) {
      normalizePipDragStepType(step.children_step)
    }
  })
}

// 校验 PIP 拖拽步骤的区域是否已框选
const validatePipDragRegions = (steps) => {
  for (const step of steps) {
    const req = step.request
    if (!req) continue
    const isPipDrag = ['PIP_SLIDER_DRAG', 'PIP_TIMELINE_DRAG'].includes(req.comparator)
    if (isPipDrag) {
      const hasOp = req.regionWidth > 0 && req.regionHeight > 0
      const hasTrack = req.trackRegionWidth > 0 && req.trackRegionHeight > 0
      if (!hasOp || !hasTrack) {
        ElMessage.warning(`步骤「${step.name}」的操作区域或轨道区域未框选，请完善后再保存`)
        return false
      }
    }
    if (step.children_step && step.children_step.length) {
      if (!validatePipDragRegions(step.children_step)) return false
    }
  }
  return true
}

const getProjectList = async () => {
  const { data } = await useProjectApi().getList({ page: 1, pageSize: 1000 })
  state.projectList = data.rows
}

// 核心保存逻辑
const saveCase = async () => {
  if (!state.form.project_id) {
    ElMessage.warning('请选择所属项目！')
    return
  }
  if (!state.form.case_category) {
    ElMessage.warning('请选择用例分类！')
    return
  }
  state.form.variables = handleEmpty(state.form.variables)
  state.form.headers = handleEmpty(state.form.headers)
  normalizePipDragStepType(state.form.step_data || [])
  if (!validatePipDragRegions(state.form.step_data || [])) return
  const res = await props.saveApi(state.form)
  state.form.id = res.data.id
  state.form.version = res.data.version
  ElMessage.success('操作成功')
  return res
}

const saveOrUpdate = () => {
  formRef.value.validate(async (valid) => {
    if (!valid) {
      ElMessage.warning('必填信息不能为空！')
      return
    }
    await saveCase()
  })
}

const handleStepDeleted = (stepData) => {
  logStep(stepData)
}

const logStep = (step) => {
  console.log('[BaseEditComponent] step deleted:', step)
}

const openRunPage = async () => {
  await saveOrUpdate()
  openRunConfigDialogRef.value?.openDialog(state.form)
}

const getEnvList = () => {
  useEnvApi().getList({ page: 1, pageSize: 1000 }).then((res) => {
    state.envList = res.data.rows
  })
}

const openReport = (reportId) => {
  state.showReportDialog = false
  router.push({ name: 'pcAutoCaseReportDetail', query: { id: reportId } })
}

const debugApiCase = () => {
  formRef.value.validate((valid) => {
    if (!valid) {
      ElMessage.warning('必填信息不能为空！')
      return
    }
    state.form.variables = handleEmpty(state.form.variables)
    state.form.headers = handleEmpty(state.form.headers)
    useApiCaseApi().debugSuites(state.form).then((req) => {
      state.reportInfo = req.data
      state.showReportDialog = true
      state.showRunPage = false
    })
  })
}

const getDataLength = (dataType) => {
  if (dataType === 'headers') return handleEmpty(state.form.headers || []).length
  if (dataType === 'variables') return handleEmpty(state.form.variables || []).length
  return 0
}

const handleAddData = (stepType) => {
  stepControllerRef.value?.handleAddData(stepType)
}

const goBack = () => {
  router.push({ name: 'apiCase' })
}

onActivated(() => {
  if (state.timestamp !== route.query.timestamp) {
    state.timestamp = route.query.timestamp
    initData()
  }
})

onMounted(() => {
  initData()
  getProjectList()
})
</script>

<style lang="scss" scoped>
.step-content {
  :deep(.el-card__body) {
    height: 100%;
  }
}

:deep(.el-dropdown) {
  vertical-align: middle;
}
</style>

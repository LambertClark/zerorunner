<template>
  <div class="app-container h100">
    <el-card class="step-content" style="height: 100%;" :body-style="{ height: 'calc(100% - 66.5px)' }">
      <template #header>
        <z-detail-page-header style="margin: 5px 0;" @back="goBack">
          <template #content>
            <span style="padding-right: 10px;">
              {{ state.editType === 'save' ? '新增' : '编辑' }}{{ caseTypeLabel }}
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
                  <template v-for="group in pcStepGroups" :key="group.groupLabel">
                    <el-dropdown-item disabled style="font-size: 12px; color: #909399;">
                      ── {{ group.groupLabel }} ──
                    </el-dropdown-item>
                    <el-dropdown-item
                        v-for="step in group.steps"
                        :key="step.step_type"
                        :style="{ color: group.color }"
                        @click="handleAddStep(step.step_type)"
                    >
                      <i :class="step.icon" style="margin-right: 6px"/>
                      {{ step.label }}
                    </el-dropdown-item>
                  </template>
                </el-dropdown-menu>
              </template>
            </el-dropdown>

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

              <el-form-item label="备注：" prop="remarks">
                <el-input v-model="state.form.remarks" placeholder="备注" clearable/>
              </el-form-item>

              <el-form-item label="步骤总数：">
                <span>{{ state.form.step_data?.length ?? 0 }}</span>
              </el-form-item>

              <!-- 扩展 slot：供子页面插入额外表单项 -->
              <slot name="extra-form" :form="state.form"/>
            </el-form>
          </div>
        </z-pane>

        <!-- 右侧步骤树 -->
        <z-pane :size="75" :min-size="50">
          <PcAutoTestStepController
              ref="stepControllerRef"
              :steps="state.form.step_data"
              :case-id="state.form.id"
              style="margin-bottom: 10px"
          />
        </z-pane>
      </z-splitpanes>
    </el-card>
  </div>
</template>

<script setup name="BaseEditComponent">
import { onActivated, onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'
import { ArrowDown } from '@element-plus/icons-vue'
import 'splitpanes/dist/splitpanes.css'
import PcAutoTestStepController from '/@/components/PcAutoTestStepController/index.vue'
import { pcStepGroups } from '/@/hooks/pcAutoTest/useMouseData.js'

const props = defineProps({
  // 'case' | 'template'
  caseType: {
    type: String,
    default: 'case',
  },
  // API 实例（由子页面传入）
  api: {
    type: Object,
    required: true,
  },
  // 返回时跳转的路由 name
  backRouteName: {
    type: String,
    required: true,
  },
})

const caseTypeLabel = props.caseType === 'template' ? 'PC 模板用例' : 'PC 用例'

const createForm = () => ({
  id: null,
  name: '',
  remarks: '',
  step_data: [],
})

const formRef = ref()
const stepControllerRef = ref()
const route = useRoute()
const router = useRouter()

const state = reactive({
  editType: 'save',
  form: createForm(),
  rules: {
    name: [{ required: true, message: '请输入用例名称', trigger: 'blur' }],
  },
  timestamp: null,
})

const initData = async () => {
  if (route.query.id) {
    state.editType = 'update'
    const getInfoFn = props.caseType === 'template'
      ? props.api.getPcTemplateInfo
      : props.api.getPcCaseInfo
    const { data } = await getInfoFn({ id: route.query.id })
    state.form = data
    if (!state.form.step_data) state.form.step_data = []
  } else {
    state.editType = route.query.editType || 'save'
    state.form = createForm()
  }
}

const saveOrUpdate = () => {
  formRef.value.validate((valid) => {
    if (!valid) {
      ElMessage.warning('必填信息不能为空！')
      return
    }
    const saveFn = props.caseType === 'template'
      ? props.api.saveOrUpdateTemplate
      : props.api.saveOrUpdate
    saveFn(state.form).then((res) => {
      state.form.id = res.data?.id ?? state.form.id
      ElMessage.success('保存成功')
    })
  })
}

const handleAddStep = (step_type) => {
  stepControllerRef.value?.handleAddData(step_type)
}

const goBack = () => {
  router.push({ name: props.backRouteName })
}

onActivated(() => {
  if (state.timestamp !== route.query.timestamp) {
    state.timestamp = route.query.timestamp
    initData()
  }
})

onMounted(() => {
  initData()
})
</script>

<style lang="scss" scoped>
.step-content {
  :deep(.el-card__body) {
    height: 100%;
  }
}
</style>

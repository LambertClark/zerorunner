<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <z-detail-page-header @back="goBack">
          <template #content>
            <span>{{ state.editType === 'save' ? '新增' : '编辑' }} PC 测试计划</span>
          </template>
          <template #extra>
            <el-button type="primary" @click="savePlan">保存</el-button>
          </template>
        </z-detail-page-header>
      </template>

      <el-form
          ref="formRef"
          :model="state.form"
          :rules="state.rules"
          label-width="90px"
          size="small"
          style="max-width: 600px"
      >
        <el-form-item label="计划名称" prop="title">
          <el-input v-model="state.form.title" placeholder="请输入计划名称" clearable/>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="state.form.desc" placeholder="描述"/>
        </el-form-item>
        <el-form-item label="启用">
          <el-switch v-model="state.form.enabled_flag" :active-value="1" :inactive-value="0"/>
        </el-form-item>
        <el-form-item label="已选用例">
          <span>{{ state.selectedCasesCount }}</span>
        </el-form-item>
      </el-form>

      <el-divider content-position="left">关联 PC 用例</el-divider>

      <div class="mb10">
        <el-input
            v-model="state.listQuery.title"
            placeholder="搜索用例名称"
            clearable
            style="width: 200px"
            @keyup.enter="search"
        />
        <el-button type="primary" class="ml10" @click="search">查询</el-button>
      </div>

      <el-row :gutter="16">
        <!-- 左：用例列表 -->
        <el-col :span="12">
          <el-card shadow="never" header="可选用例">
            <el-table
                ref="caseTableRef"
                :data="state.listData"
                height="360px"
                @selection-change="selectionChange"
            >
              <el-table-column type="selection" width="50"/>
              <el-table-column label="用例名称" prop="name"/>
              <el-table-column label="操作" width="70" fixed="right">
                <template #default="{ row }">
                  <el-button type="primary" size="small" @click="addCase(row)">添加</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>

        <!-- 右：已选用例 -->
        <el-col :span="12">
          <el-card shadow="never" :header="`已选用例（${state.selectedCasesCount}）`">
            <el-table :data="state.selectedCases" height="360px">
              <el-table-column label="序号" type="index" width="50"/>
              <el-table-column label="用例名称" prop="name"/>
              <el-table-column label="操作" width="70" fixed="right">
                <template #default="{ row, $index }">
                  <el-button type="danger" size="small" @click="removeCase($index)">移除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup name="EditPcPlan">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'
import { usePcPlanApi } from '/@/api/usePcAutoApi/pcPlan'
import { usePcTestCaseApi } from '/@/api/usePcAutoApi/pcTestCase'
import { handleEmpty } from '/@/utils/other'

const formRef = ref()
const caseTableRef = ref()
const route = useRoute()
const router = useRouter()

const state = reactive({
  editType: 'save',
  form: {
    id: null,
    title: '',
    desc: '',
    enabled_flag: 1,
  },
  rules: {
    title: [{ required: true, message: '请输入计划名称', trigger: 'blur' }],
  },
  selectedCases: [],
  selectedCasesCount: 0,
  listData: [],
  listQuery: {
    page: 1,
    pageSize: 100,
    title: '',
    is_template: false,
  },
})

const getPlanDetail = async () => {
  if (route.query.id) {
    state.editType = 'update'
    const { data } = await usePcPlanApi().getPcPlanDetail({ id: route.query.id })
    state.selectedCases = data.cases || []
    state.form = {
      id: data.id,
      title: data.title,
      desc: data.desc,
      enabled_flag: data.enabled_flag ?? 1,
    }
    updateSelectionCasesCount()
  } else {
    state.editType = route.query.editType || 'save'
  }
}

const initSelectedCases = () => {
  state.selectedCases = []
  updateSelectionCasesCount()
}

const search = () => {
  state.listQuery.page = 1
  getList()
}

const getList = () => {
  usePcTestCaseApi().getPcCaseList(state.listQuery).then((res) => {
    state.listData = res.data.rows
  })
}

const selectionChange = (selection) => {
  // 批量添加选中行（避免重复）
  selection.forEach((row) => addCase(row))
}

const updateSelectionCasesCount = () => {
  state.selectedCasesCount = state.selectedCases.length
}

const addCase = (row) => {
  if (state.selectedCases.some((c) => c.id === row.id)) return
  state.selectedCases.push({ id: row.id, name: row.name })
  updateSelectionCasesCount()
}

const removeCase = (idx) => {
  state.selectedCases.splice(idx, 1)
  updateSelectionCasesCount()
}

const savePlan = () => {
  formRef.value.validate((valid) => {
    if (!valid) return
    const planForm = {
      id: state.form.id,
      title: state.form.title,
      desc: state.form.desc,
      enabled_flag: state.form.enabled_flag,
      cases: state.selectedCases,
    }
    usePcPlanApi().saveOrUpdate(planForm).then((res) => {
      state.form.id = res.data?.id ?? state.form.id
      ElMessage.success('保存成功')
    })
  })
}

const goBack = () => {
  router.push({ name: 'pcAutoPlanList' })
}

onMounted(async () => {
  await getPlanDetail()
  getList()
})
</script>

<style lang="scss" scoped></style>

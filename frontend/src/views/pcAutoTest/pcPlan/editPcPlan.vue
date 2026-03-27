<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <z-detail-page-header @back="goBack">
          <template #content>
            <span>{{ state.editType === 'save' ? '新增' : '编辑' }} PC 测试计划</span>
          </template>
          <template #extra>
            <el-button type="primary" @click="saveOrUpdate">保存</el-button>
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
        <el-form-item label="计划名称" prop="name">
          <el-input v-model="state.form.name" placeholder="请输入计划名称" clearable/>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="state.form.remarks" placeholder="备注"/>
        </el-form-item>
      </el-form>

      <el-divider content-position="left">关联 PC 用例</el-divider>

      <div class="mb10">
        <el-input
            v-model="state.searchName"
            placeholder="搜索用例名称"
            clearable
            style="width: 200px"
            @keyup.enter="searchCases"
        />
        <el-button type="primary" class="ml10" @click="searchCases">查询</el-button>
      </div>

      <el-row :gutter="16">
        <!-- 左：用例列表 -->
        <el-col :span="12">
          <el-card shadow="never" header="可选用例">
            <el-table
                :data="state.caseList"
                height="360px"
                @row-click="addCase"
            >
              <el-table-column label="用例名称" prop="name"/>
              <el-table-column label="操作" width="70" fixed="right">
                <template #default="{ row }">
                  <el-button type="primary" size="small" @click.stop="addCase(row)">添加</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>

        <!-- 右：已选用例 -->
        <el-col :span="12">
          <el-card shadow="never" :header="`已选用例（${state.form.case_list?.length ?? 0}）`">
            <el-table :data="state.form.case_list" height="360px">
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

<script setup name="editPcPlan">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'
import { usePcPlanApi } from '/@/api/usePcAutoApi/pcPlan.js'
import { usePcTestCaseApi } from '/@/api/usePcAutoApi/pcTestCase.js'

const formRef = ref()
const route = useRoute()
const router = useRouter()

const createForm = () => ({
  id: null,
  name: '',
  remarks: '',
  case_list: [],
})

const state = reactive({
  editType: 'save',
  form: createForm(),
  rules: {
    name: [{ required: true, message: '请输入计划名称', trigger: 'blur' }],
  },
  caseList: [],
  searchName: '',
})

const initData = async () => {
  if (route.query.id) {
    state.editType = 'update'
    const { data } = await usePcPlanApi().getPlanInfo({ id: route.query.id })
    state.form = data
    if (!state.form.case_list) state.form.case_list = []
  } else {
    state.editType = route.query.editType || 'save'
    state.form = createForm()
  }
  searchCases()
}

const searchCases = () => {
  usePcTestCaseApi().getList({ page: 1, pageSize: 100, name: state.searchName })
    .then((res) => {
      state.caseList = res.data.rows
    })
}

const addCase = (row) => {
  if (state.form.case_list.some((c) => c.id === row.id)) {
    ElMessage.warning('该用例已添加')
    return
  }
  state.form.case_list.push({ id: row.id, name: row.name })
}

const removeCase = (idx) => {
  state.form.case_list.splice(idx, 1)
}

const saveOrUpdate = () => {
  formRef.value.validate((valid) => {
    if (!valid) return
    usePcPlanApi().saveOrUpdate(state.form).then((res) => {
      state.form.id = res.data?.id ?? state.form.id
      ElMessage.success('保存成功')
    })
  })
}

const goBack = () => {
  router.push({ name: 'pcAutoPlanList' })
}

onMounted(() => {
  initData()
})
</script>

<style lang="scss" scoped></style>

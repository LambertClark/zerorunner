<template>
  <div class="case-template-controller">
    <el-form label-width="90px" size="small">
      <el-form-item label="模板用例">
        <el-input
            v-model="data.pc_request.case_template_name"
            placeholder="请输入模板用例名称搜索"
            clearable
        >
          <template #append>
            <el-button @click="state.showTemplateDialog = true">选择</el-button>
          </template>
        </el-input>
      </el-form-item>

      <el-form-item label="已选模板" v-if="data.pc_request.case_template_id">
        <el-tag type="success">{{ data.pc_request.case_template_name }}</el-tag>
        <el-button
            type="danger"
            link
            size="small"
            style="margin-left: 8px"
            @click="clearTemplate"
        >清除</el-button>
      </el-form-item>
    </el-form>

    <!-- 模板用例选择弹窗 -->
    <el-dialog
        v-model="state.showTemplateDialog"
        title="选择 PC 模板用例"
        width="700px"
        append-to-body
        destroy-on-close
    >
      <div style="margin-bottom: 10px">
        <el-input
            v-model="state.searchName"
            placeholder="搜索模板用例名称"
            clearable
            style="width: 240px"
            @keyup.enter="fetchTemplates"
        />
        <el-button type="primary" class="ml10" @click="fetchTemplates">查询</el-button>
      </div>
      <el-table :data="state.templateList" height="360px" @row-click="selectTemplate">
        <el-table-column label="序号" type="index" width="60"/>
        <el-table-column label="模板名称" prop="name"/>
        <el-table-column label="备注" prop="remarks"/>
        <el-table-column label="操作" width="80" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="selectTemplate(row)">选择</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
          v-model:current-page="state.page"
          v-model:page-size="state.pageSize"
          :total="state.total"
          layout="prev, pager, next"
          style="margin-top: 10px; text-align: right"
          @current-change="fetchTemplates"
      />
    </el-dialog>
  </div>
</template>

<script setup name="CaseTemplateController">
import { reactive, onMounted } from 'vue'
import { usePcTestCaseApi } from '/@/api/usePcAutoApi/pcTestCase.js'

const props = defineProps({
  data: {
    type: Object,
    default: () => ({}),
  },
})

const state = reactive({
  showTemplateDialog: false,
  searchName: '',
  templateList: [],
  page: 1,
  pageSize: 10,
  total: 0,
})

const fetchTemplates = () => {
  usePcTestCaseApi().getPcTemplateList({
    page: state.page,
    pageSize: state.pageSize,
    name: state.searchName,
  }).then((res) => {
    state.templateList = res.data.rows
    state.total = res.data.rowTotal
  })
}

const selectTemplate = (row) => {
  props.data.pc_request.case_template_id = row.id
  props.data.pc_request.case_template_name = row.name
  state.showTemplateDialog = false
}

const clearTemplate = () => {
  props.data.pc_request.case_template_id = null
  props.data.pc_request.case_template_name = ''
}

onMounted(() => {
  fetchTemplates()
})
</script>

<style lang="scss" scoped>
.case-template-controller {
  padding: 0 4px;
}
</style>

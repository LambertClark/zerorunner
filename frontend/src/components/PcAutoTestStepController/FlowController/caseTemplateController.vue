<template>
  <div class="case-template-controller">
    <div style="display: flex; align-items: center; gap: 8px;">
      <el-select
          v-model="data.pc_request.case_template_id"
          placeholder="请选择模板用例"
          filterable
          clearable
          style="flex: 1;"
          @change="handleTemplateChange"
      >
        <el-option
            v-for="opt in caseTemplateOptions"
            :key="opt.id"
            :label="opt.title || opt.name"
            :value="opt.id"
        />
      </el-select>
      <el-button type="primary" size="small" @click="getPcCaseList">查询</el-button>
    </div>
  </div>
</template>

<script setup name="caseTemplateController">
import { reactive, ref, onMounted } from 'vue'
import { usePcTestCaseApi } from '/@/api/usePcAutoApi/pcTestCase.js'

const props = defineProps({
  data: { type: Object, required: true },
})
const emit = defineEmits(['template-selected'])

const caseTemplateOptions = ref([])

const state = reactive({
  listQuery: {
    page: 1,
    pageSize: 50,
    title: '',
    is_template: 1,
    created_by: '',
    prioritys: [],
    module: null,
  },
})

const getPcCaseList = () => {
  usePcTestCaseApi().getPcCaseList(state.listQuery).then((res) => {
    caseTemplateOptions.value = res.data.rows || []
  })
}

const handleTemplateChange = (id) => {
  const selectedItem = caseTemplateOptions.value.find((item) => item.id === id)
  if (selectedItem && selectedItem.step_data) {
    props.data.children = [...selectedItem.step_data]
    props.data.children_steps = [...selectedItem.step_data]
    emit('template-selected', selectedItem)
  }
}

onMounted(() => { getPcCaseList() })
</script>

<style lang="scss" scoped>
.case-template-controller {
  padding: 4px 0;
}
</style>

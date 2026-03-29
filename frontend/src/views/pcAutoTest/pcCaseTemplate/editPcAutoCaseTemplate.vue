<template>
  <BaseEditComponent
      page-title="PC 模板用例"
      :create-form-data="createForm"
      :save-api="usePcTestCaseApi().saveOrUpdate"
      :get-case-info-api="usePcTestCaseApi().getCaseInfo"
      :left-components="leftComponents"
  />
</template>

<script setup name="editPcAutoCaseTemplate">
import BaseEditComponent from '/@/views/pcAutoTest/component/pcCaseEdit/BaseEditComponent.vue'
import { usePcTestCaseApi } from '/@/api/usePcAutoApi/pcTestCase'
import { mouseComponents, keyboardComponents, flowComponents } from '/@/components/generator/config'

const createForm = () => ({
  name: '',
  env_id: null,
  step_rely: 1,
  project_id: '',
  remarks: '',
  step_data: [],
  variables: [],
  headers: [],
  is_template: 1,
})

const leftComponents = [
  { label: '鼠标操作', items: mouseComponents },
  { label: '键盘操作', items: keyboardComponents },
  { label: '流程控制', items: flowComponents },
]
</script>

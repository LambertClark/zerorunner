<template>
  <BasePcCaseList
      case-type="template"
      edit-route-name="editPcAutoCaseTemplate"
      :api="api"
      :show-run="false"
  />
</template>

<script setup name="pcAutoCaseListTemplate">
import BasePcCaseList from '/@/views/pcAutoTest/component/pcCaseEdit/BasePcCaseList.vue'
import { usePcTestCaseApi } from '/@/api/usePcAutoApi/pcTestCase.js'

const api = usePcTestCaseApi()
</script>

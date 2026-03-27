<template>
  <BaseEditComponent
      case-type="template"
      :api="api"
      back-route-name="pcAutoCaseListTemplate"
  />
</template>

<script setup name="editPcAutoCaseTemplate">
import BaseEditComponent from '/@/views/pcAutoTest/component/pcCaseEdit/BaseEditComponent.vue'
import { usePcTestCaseApi } from '/@/api/usePcAutoApi/pcTestCase.js'

const api = usePcTestCaseApi()
</script>

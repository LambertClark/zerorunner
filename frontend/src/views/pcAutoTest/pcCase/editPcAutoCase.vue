<template>
  <BaseEditComponent
      case-type="case"
      :api="api"
      back-route-name="pcAutoCaseList"
  />
</template>

<script setup name="editPcAutoCase">
import BaseEditComponent from '/@/views/pcAutoTest/component/pcCaseEdit/BaseEditComponent.vue'
import { usePcTestCaseApi } from '/@/api/usePcAutoApi/pcTestCase.js'

const api = usePcTestCaseApi()
</script>

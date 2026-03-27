<template>
  <BasePcCaseList
      case-type="case"
      edit-route-name="editPcAutoCase"
      :api="api"
      :show-run="true"
  />
</template>

<script setup name="pcAutoCaseList">
import BasePcCaseList from '/@/views/pcAutoTest/component/pcCaseEdit/BasePcCaseList.vue'
import { usePcTestCaseApi } from '/@/api/usePcAutoApi/pcTestCase.js'

const api = usePcTestCaseApi()
</script>

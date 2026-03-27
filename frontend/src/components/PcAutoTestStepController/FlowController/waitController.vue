<template>
  <div class="wait-controller">
    <el-form label-width="90px" size="small">
      <el-form-item label="等待时间(s)">
        <el-input-number
            v-model="data.pc_request.wait_time"
            :min="0.1"
            :max="3600"
            :step="0.5"
            style="width: 100%"
        />
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup name="WaitController">
const props = defineProps({
  data: {
    type: Object,
    default: () => ({}),
  },
})
</script>

<style lang="scss" scoped>
.wait-controller {
  padding: 0 4px;
}
</style>

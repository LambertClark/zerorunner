<template>
  <div class="app-container">
    <el-button type="primary" @click="centerDialogVisible = true">打开对话框</el-button>

    <el-dialog v-model="centerDialogVisible" title="测试表单" width="500px" align-center>
      <el-form ref="ruleFormRef" :model="ruleForm" :rules="rules" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="ruleForm.name" placeholder="请输入名称"/>
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="ruleForm.type" placeholder="请选择类型" style="width: 100%">
            <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="ruleForm.remark" type="textarea" placeholder="请输入备注"/>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="resetForm(ruleFormRef)">重置</el-button>
          <el-button type="primary" @click="submitForm(ruleFormRef)">提交</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'

const centerDialogVisible = ref(false)
const ruleFormRef = ref()

const ruleForm = reactive({
  name: '',
  type: '',
  remark: '',
})

const rules = {
  name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择类型', trigger: 'change' }],
}

const options = [
  { label: '类型A', value: 'a' },
  { label: '类型B', value: 'b' },
  { label: '类型C', value: 'c' },
]

const submitForm = (formEl) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      ElMessage.success('提交成功')
      centerDialogVisible.value = false
    }
  })
}

const resetForm = (formEl) => {
  if (!formEl) return
  formEl.resetFields()
}
</script>

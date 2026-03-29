<template>
  <div class="system-edit-menu-container">
    <el-dialog
        draggable
        :title="state.editType === 'save' ? '新增菜单' : '修改菜单'"
        v-model="state.isShowDialog"
        width="769px"
    >
      <el-form :model="state.form" :rules="state.rules" size="default" label-width="80px">
        <el-row :gutter="35">
          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="上级菜单" prop="parent_id">
              <el-tree-select
                  ref="menuTreeRef"
                  filterable
                  v-model="state.form.parent_id"
                  :data="menuTree"
                  :props="{ label: 'title', value: 'id' }"
                  check-strictly
                  :render-after-expand="false"
              />
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
            <el-form-item label="菜单类型" prop="menu_type">
              <el-radio-group v-model="state.form.menu_type">
                <el-radio :label="10">菜单</el-radio>
                <el-radio :label="20">按钮</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="菜单名称" prop="title">
              <el-input v-model="state.form.title" placeholder="格式：message.router.xxx" clearable></el-input>
            </el-form-item>
          </el-col>
          <template v-if="state.form.menu_type === 10">
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="路由名称" prop="name">
                <el-input v-model="state.form.name" placeholder="路由中的 name 值" clearable></el-input>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="路由路径" prop="path">
                <el-input v-model="state.form.path" placeholder="路由中的 path 值" clearable></el-input>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="重定向">
                <el-input v-model="state.form.redirect" placeholder="请输入路由重定向" clearable></el-input>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="菜单图标">
                <IconSelector placeholder="请输入菜单图标" v-model="state.form.icon" type="all"/>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="组件路径" prop="component">
                <el-input v-model="state.form.component" placeholder="组件路径" clearable></el-input>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="链接地址">
                <el-input
                    v-model="state.form.linkUrl"
                    placeholder="外链/内嵌时链接地址（http:xxx.com）"
                    clearable
                    :disabled="!state.form.isLink"
                ></el-input>
              </el-form-item>
            </el-col>
          </template>
          <template v-if="state.form.menu_type === 20">
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="权限标识">
                <el-input v-model="state.form.btnPower" placeholder="请输入权限标识" clearable></el-input>
              </el-form-item>
            </el-col>
          </template>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="菜单排序">
              <el-input-number v-model="state.form.sort" controls-position="right" placeholder="请输入排序" class="w100"/>
            </el-form-item>
          </el-col>
          <template v-if="state.form.menu_type === 10">
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="是否隐藏">
                <el-radio-group v-model="state.form.isHide">
                  <el-radio :label="true">隐藏</el-radio>
                  <el-radio :label="false">不隐藏</el-radio>
                </el-radio-group>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="页面缓存">
                <el-radio-group v-model="state.form.isKeepAlive">
                  <el-radio :label="true">缓存</el-radio>
                  <el-radio :label="false">不缓存</el-radio>
                </el-radio-group>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="是否固定">
                <el-radio-group v-model="state.form.isAffix">
                  <el-radio :label="true">固定</el-radio>
                  <el-radio :label="false">不固定</el-radio>
                </el-radio-group>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="是否外链">
                <el-radio-group v-model="state.form.isLink" :disabled="state.form.isIframe">
                  <el-radio :label="true">是</el-radio>
                  <el-radio :label="false">否</el-radio>
                </el-radio-group>
              </el-form-item>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
              <el-form-item label="是否内嵌">
                <el-radio-group v-model="state.form.isIframe" @change="onSelectIframeChange">
                  <el-radio :label="true">是</el-radio>
                  <el-radio :label="false">否</el-radio>
                </el-radio-group>
              </el-form-item>
            </el-col>
          </template>
        </el-row>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="onCancel">取 消</el-button>
          <el-button type="primary" @click="saveOrUpdate">保 存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="SaveOrUpdateMenu">
import { computed, nextTick, onMounted, reactive, ref } from 'vue'
import IconSelector from '/@/components/iconSelector/index.vue'
import { useMenuApi } from '/@/api/useSystemApi/menu'
import { ElMessage } from 'element-plus'

const menuTreeRef = ref()

const emit = defineEmits(['getList'])
const props = defineProps({
  allMenuList: {
    type: Array,
  },
  menuList: {
    type: Array,
    default: () => [],
  },
})

const menuTree = computed(() => {
  return [{ title: '根目录', id: 0, children: [...props.menuList] }]
})

const createMenuForm = () => {
  return {
    id: null,
    parent_id: 0,
    menu_type: 10,
    name: '',
    meta: {},
    component: '',
    sort: 0,
    path: '',
    redirect: '',
    title: '',
    icon: '',
    isHide: false,
    isKeepAlive: true,
    isAffix: false,
    isLink: false,
    linkUrl: '',
    isIframe: false,
    roles: '',
    btnPower: '',
  }
}

const state = reactive({
  isShowDialog: false,
  editType: '',
  form: createMenuForm(),
  rules: {
    name: [{ required: true, message: '请输入路由名称', trigger: 'blur' }],
    parent_id: [{ required: true, message: '请选择上级菜单', trigger: 'blur' }],
    menu_type: [{ required: true, message: '请选择菜单类型', trigger: 'blur' }],
    component: [{ required: true, message: '请输入组件路径', trigger: 'blur' }],
    path: [{ required: true, message: '请输入路由路径', trigger: 'blur' }],
    title: [{ required: true, message: '请输入菜单名称', trigger: 'blur' }],
  },
})

const openDialog = (editType, row) => {
  state.editType = editType
  if (row) {
    state.form = JSON.parse(JSON.stringify(row))
  } else {
    state.form = createMenuForm()
  }
  state.isShowDialog = true
  nextTick(() => {
    menuTreeRef.value?.setCurrentKey(state.form.parent_id)
  })
}

const closeDialog = () => {
  state.isShowDialog = false
}

const onSelectIframeChange = () => {
  if (state.form.isIframe) state.form.isLink = true
  else state.form.isLink = false
}

const onCancel = () => {
  closeDialog()
}

const saveOrUpdate = () => {
  useMenuApi()
    .saveOrUpdate(state.form)
    .then(() => {
      ElMessage.success('操作成功')
      emit('getList')
      closeDialog()
    })
}

onMounted(() => {})

defineExpose({
  openDialog,
})
</script>

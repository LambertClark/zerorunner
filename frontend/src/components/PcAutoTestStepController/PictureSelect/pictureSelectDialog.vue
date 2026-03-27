<template>
  <el-dialog
      v-model="dialogVisible"
      title="选择图片素材"
      width="800px"
      append-to-body
      destroy-on-close
      :close-on-click-modal="false"
  >
    <div style="display: flex; gap: 12px; height: 480px;">
      <!-- 左侧素材树 -->
      <div style="width: 200px; border-right: 1px solid #eee; overflow-y: auto; padding-right: 8px;">
        <el-tree
            :data="state.treeData"
            :props="{ label: 'name', children: 'children' }"
            node-key="id"
            highlight-current
            @node-click="handleTreeClick"
        />
      </div>

      <!-- 右侧素材列表 -->
      <div style="flex: 1; overflow-y: auto;">
        <div style="margin-bottom: 10px;">
          <el-input
              v-model="state.searchName"
              placeholder="搜索素材名称"
              clearable
              style="width: 200px"
              @keyup.enter="fetchPictures"
          />
          <el-button type="primary" class="ml10" @click="fetchPictures">查询</el-button>
        </div>

        <div class="picture-grid">
          <div
              v-for="pic in state.pictureList"
              :key="pic.id"
              class="picture-item"
              :class="{ 'picture-item--selected': state.selectedId === pic.id }"
              @click="selectPicture(pic)"
          >
            <el-image
                :src="getPicUrl(pic)"
                fit="contain"
                style="width: 100%; height: 80px;"
                :preview-src-list="[getPicUrl(pic)]"
                preview-teleported
                @click.stop
            />
            <div class="picture-item__name">{{ pic.name }}</div>
          </div>
        </div>

        <el-empty v-if="state.pictureList.length === 0" description="暂无素材"/>

        <el-pagination
            v-model:current-page="state.page"
            v-model:page-size="state.pageSize"
            :total="state.total"
            layout="prev, pager, next"
            style="margin-top: 10px"
            @current-change="fetchPictures"
        />
      </div>
    </div>

    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button
          type="primary"
          :disabled="!state.selectedPicture"
          @click="confirmSelect"
      >确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup name="PictureSelectDialog">
import { reactive, computed, onMounted } from 'vue'
import { usePcPictureApi } from '/@/api/usePcAutoApi/pcPicture.js'
import { getBaseApiUrl } from '/@/utils/config'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:visible', 'select'])

const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => emit('update:visible', val),
})

const state = reactive({
  treeData: [],
  pictureList: [],
  searchName: '',
  selectedTreeId: null,
  selectedId: null,
  selectedPicture: null,
  page: 1,
  pageSize: 20,
  total: 0,
})

const getPicUrl = (pic) => {
  const url = pic.file_path || pic.url || ''
  if (!url) return ''
  return url.startsWith('http') ? url : `${getBaseApiUrl()}/${url}`
}

const fetchTree = () => {
  usePcPictureApi().getTreeList({}).then((res) => {
    state.treeData = res.data || []
  })
}

const fetchPictures = () => {
  usePcPictureApi().getPictureList({
    page: state.page,
    pageSize: state.pageSize,
    name: state.searchName,
    tree_id: state.selectedTreeId,
  }).then((res) => {
    state.pictureList = res.data.rows || []
    state.total = res.data.rowTotal || 0
  })
}

const handleTreeClick = (node) => {
  state.selectedTreeId = node.id
  state.page = 1
  fetchPictures()
}

const selectPicture = (pic) => {
  state.selectedId = pic.id
  state.selectedPicture = pic
}

const confirmSelect = () => {
  if (state.selectedPicture) {
    emit('select', state.selectedPicture)
    emit('update:visible', false)
  }
}

onMounted(() => {
  fetchTree()
  fetchPictures()
})
</script>

<style lang="scss" scoped>
.picture-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 10px;
}

.picture-item {
  border: 2px solid #eee;
  border-radius: 6px;
  padding: 6px;
  cursor: pointer;
  transition: border-color 0.2s;

  &:hover {
    border-color: #409EFF;
  }

  &--selected {
    border-color: #409EFF;
    background: #ecf5ff;
  }

  .picture-item__name {
    font-size: 12px;
    text-align: center;
    margin-top: 4px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    color: #606266;
  }
}
</style>

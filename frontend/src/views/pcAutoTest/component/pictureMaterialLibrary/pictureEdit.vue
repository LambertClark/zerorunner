<template>
  <div class="picture-edit-panel">
    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-input
        v-model="filterText"
        placeholder="搜索图片名称"
        clearable
        size="small"
        style="width: 200px"
      />
      <el-radio-group v-model="searchLocalImage" size="small" style="margin-left: 12px">
        <el-radio-button :value="true">节点搜索</el-radio-button>
        <el-radio-button :value="false">全局搜索</el-radio-button>
      </el-radio-group>
    </div>

    <!-- 本地模式 -->
    <template v-if="searchLocalImage">
      <div class="node-path" v-if="currentNode">当前路径：{{ currentNode.full_path }}</div>
      <div class="picture-grid" v-if="imageList.length > 0">
        <div v-for="(img, index) in imageList" :key="img.id" class="picture-item">
          <el-image
            :src="img.image_url"
            fit="contain"
            class="picture-item__img"
            @click="handlePreview(index)"
          />
          <div class="picture-item__name" :title="img.name">{{ img.name }}</div>
          <div class="picture-item__actions">
            <el-button size="small" type="primary" link @click="handlePreview(index)">预览</el-button>
            <el-button size="small" type="warning" link @click="handleEditName(index)">编辑</el-button>
            <el-button size="small" type="danger" link @click="handleDelete(index)">删除</el-button>
          </div>
        </div>
      </div>
      <el-empty v-else description="暂无素材" />
    </template>

    <!-- 全局模式 -->
    <template v-else>
      <template v-if="treeImageList.length > 0">
        <div v-for="(tree, treeIndex) in treeImageList" :key="tree.id" class="tree-group">
          <div class="tree-group-title">{{ tree.name }}</div>
          <div class="picture-grid" v-if="tree.picture_data && tree.picture_data.length > 0">
            <div v-for="(pic, picIndex) in tree.picture_data" :key="pic.id" class="picture-item">
              <el-image
                :src="pic.image_url"
                fit="contain"
                class="picture-item__img"
                @click="handleTreePreview(treeIndex, picIndex)"
              />
              <div class="picture-item__name" :title="pic.name">{{ pic.name }}</div>
              <div class="picture-item__actions">
                <el-button size="small" type="primary" link @click="handleTreePreview(treeIndex, picIndex)">预览</el-button>
                <el-button size="small" type="warning" link @click="handleEditTreeImage(treeIndex, picIndex)">编辑</el-button>
                <el-button size="small" type="danger" link @click="handleDeleteTreeImage(treeIndex, picIndex)">删除</el-button>
              </div>
            </div>
          </div>
          <el-empty v-else description="该节点暂无素材" :image-size="60" />
        </div>
      </template>
      <el-empty v-else-if="filterText" description="未找到相关素材" />
      <el-empty v-else description="请输入关键字搜索" />
    </template>

    <!-- 图片预览器 -->
    <el-image-viewer
      v-if="showViewer"
      :url-list="previewList"
      :initial-index="currentIndex"
      @close="showViewer = false"
    />

    <!-- 编辑素材弹窗 -->
    <FormEditPicture ref="editPictureForm" @updateImage="handleUpdateImage" />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import emitter from '/@/utils/mitt.js'
import { usePcPictureApi } from '/@/api/usePcAutoApi/pcPicture.js'
import { deepClone } from '/@/utils/other.js'
import FormEditPicture from './form/formEditPicture.vue'

const originalList = ref([])
const imageList = ref([])
const treeImageList = ref([])
const currentNode = ref(null)
const searchLocalImage = ref(true)
const filterText = ref('')
const editPictureForm = ref()
const showViewer = ref(false)
const currentIndex = ref(0)

const previewList = computed(() => {
  if (searchLocalImage.value) {
    return imageList.value.map((img) => img.image_url)
  }
  return treeImageList.value.flatMap((tree) => tree.picture_data.map((pic) => pic.image_url))
})

watch([filterText, searchLocalImage], ([text, isLocal]) => {
  if (!text) {
    if (isLocal) {
      imageList.value = deepClone(originalList.value)
    } else {
      treeImageList.value = []
    }
    return
  }
  if (isLocal) {
    imageList.value = originalList.value.filter((img) => img.name?.includes(text))
  } else {
    usePcPictureApi()
      .pictureByName({ picture_name: text })
      .then((res) => {
        treeImageList.value = res.data || []
      })
  }
})

emitter.on('picture-edit', (data) => {
  currentNode.value = data.currentNode
  originalList.value = deepClone(data.imageList)
  imageList.value = deepClone(data.imageList)
})

function handlePreview(index) {
  currentIndex.value = index
  showViewer.value = true
}

function handleTreePreview(treeIndex, picIndex) {
  let flatIndex = 0
  for (let i = 0; i < treeIndex; i++) {
    flatIndex += treeImageList.value[i].picture_data.length
  }
  flatIndex += picIndex
  currentIndex.value = flatIndex
  showViewer.value = true
}

function handleDelete(index) {
  const temp = imageList.value[index]
  ElMessageBox.confirm('确定删除该素材？', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    usePcPictureApi()
      .deletePicture({ id: temp.id })
      .then(() => {
        imageList.value.splice(index, 1)
        originalList.value = originalList.value.filter((img) => img.id !== temp.id)
        ElMessage.success('删除成功')
      })
  })
}

function handleDeleteTreeImage(treeIndex, picIndex) {
  const temp = treeImageList.value[treeIndex].picture_data[picIndex]
  ElMessageBox.confirm('确定删除该素材？', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    usePcPictureApi()
      .deletePicture({ id: temp.id })
      .then(() => {
        treeImageList.value[treeIndex].picture_data.splice(picIndex, 1)
        ElMessage.success('删除成功')
      })
  })
}

function handleEditName(index) {
  editPictureForm.value.openDialog(imageList.value[index], { treeIndex: null, pictureDataIndex: index })
}

function handleEditTreeImage(treeIndex, pictureDataIndex) {
  const pic = treeImageList.value[treeIndex].picture_data[pictureDataIndex]
  editPictureForm.value.openDialog(pic, { treeIndex, pictureDataIndex })
}

function handleUpdateImage(imageData, indexData) {
  if (indexData.treeIndex !== null) {
    treeImageList.value[indexData.treeIndex].picture_data[indexData.pictureDataIndex] = imageData
  } else {
    imageList.value[indexData.pictureDataIndex] = imageData
    originalList.value[indexData.pictureDataIndex] = imageData
  }
}
</script>

<style lang="scss" scoped>
.picture-edit-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.search-bar {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  flex-shrink: 0;
}

.node-path {
  font-size: 12px;
  color: #909399;
  margin-bottom: 8px;
  flex-shrink: 0;
}

.tree-group {
  margin-bottom: 16px;
}

.tree-group-title {
  font-weight: 600;
  font-size: 13px;
  color: #303133;
  margin-bottom: 8px;
  padding-left: 4px;
  border-left: 3px solid #409eff;
}

.picture-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 12px;
  margin-bottom: 8px;
}

.picture-item {
  border: 1px solid #eee;
  border-radius: 6px;
  padding: 8px;
  text-align: center;
  transition: box-shadow 0.2s;

  &:hover {
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.12);
  }

  &__img {
    width: 100%;
    height: 100px;
    cursor: pointer;
  }

  &__name {
    font-size: 12px;
    color: #606266;
    margin: 4px 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  &__actions {
    display: flex;
    gap: 2px;
    justify-content: center;
    flex-wrap: wrap;
  }
}
</style>

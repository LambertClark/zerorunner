<template>
  <div class="app-container h100">
    <el-card style="height: 100%;" :body-style="{ height: 'calc(100% - 56px)', display: 'flex', gap: '12px' }">
      <!-- 左侧：素材树 -->
      <div style="width: 220px; border-right: 1px solid #eee; padding-right: 12px; overflow-y: auto; flex-shrink: 0;">
        <PictureTree ref="treeRef" />
      </div>

      <!-- 右侧：素材面板 -->
      <div style="flex: 1; overflow-y: auto;">
        <PictureEdit />
      </div>
    </el-card>
  </div>
</template>

<script setup name="pictureMaterialLibrary">
import PictureTree from '/@/views/pcAutoTest/component/pictureMaterialLibrary/pictureTree.vue'
import PictureEdit from '/@/views/pcAutoTest/component/pictureMaterialLibrary/pictureEdit.vue'

const treeRef = null
</script>

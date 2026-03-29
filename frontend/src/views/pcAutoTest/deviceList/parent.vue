<template>
  <div class="device-parent-layout">
    <el-container>
      <!-- 左侧导航 -->
      <el-aside width="200px">
        <el-menu
            :default-active="activeMenu"
            @select="handleMenuSelect"
        >
          <el-menu-item index="/pcAutoTest/deviceList">
            <el-icon><Monitor/></el-icon>
            <span>设备列表</span>
          </el-menu-item>
          <el-menu-item index="/pcAutoTest/deviceList/status">
            <el-icon><DataLine/></el-icon>
            <span>状态统计</span>
          </el-menu-item>
          <el-menu-item index="/pcAutoTest/deviceList/batch-connect">
            <el-icon><Connection/></el-icon>
            <span>批量连接</span>
          </el-menu-item>
          <el-menu-item index="/pcAutoTest/deviceList/batch-test">
            <el-icon><VideoPlay/></el-icon>
            <span>批量测试</span>
          </el-menu-item>
          <el-menu-item index="/pcAutoTest/deviceList/settings">
            <el-icon><Setting/></el-icon>
            <span>设备设置</span>
          </el-menu-item>
          <el-menu-item index="/pcAutoTest/deviceList/logs">
            <el-icon><Document/></el-icon>
            <span>操作日志</span>
          </el-menu-item>
          <el-menu-item index="/pcAutoTest/deviceList/reports">
            <el-icon><DataAnalysis/></el-icon>
            <span>测试报告</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 右侧内容 -->
      <el-main>
        <router-view/>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  Monitor,
  DataLine,
  Connection,
  VideoPlay,
  Setting,
  Document,
  DataAnalysis,
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const routeMap = {
  '/pcAutoTest/deviceList': '/pcAutoTest/deviceList',
  '/pcAutoTest/deviceList/status': '/pcAutoTest/deviceList/status',
  '/pcAutoTest/deviceList/batch-connect': '/pcAutoTest/deviceList/batch-connect',
  '/pcAutoTest/deviceList/batch-test': '/pcAutoTest/deviceList/batch-test',
  '/pcAutoTest/deviceList/settings': '/pcAutoTest/deviceList/settings',
  '/pcAutoTest/deviceList/logs': '/pcAutoTest/deviceList/logs',
  '/pcAutoTest/deviceList/reports': '/pcAutoTest/deviceList/reports',
}

const activeMenu = ref(route.path)

const handleMenuSelect = (index) => {
  router.push(index)
}

watch(
  () => route.path,
  (path) => {
    activeMenu.value = routeMap[path] || '/pcAutoTest/deviceList'
  }
)
</script>

<style lang="scss" scoped>
.device-parent-layout {
  height: 100%;

  .el-container {
    height: 100%;
  }

  .el-aside {
    border-right: 1px solid #e4e7ed;
    background: #fff;
  }

  .el-menu {
    border-right: none;
  }
}
</style>

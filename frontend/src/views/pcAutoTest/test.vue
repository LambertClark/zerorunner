<template>
  <div class="app-container">
    <el-popover
        v-model:visible="popoverVisible"
        placement="bottom"
        width="400"
        trigger="click"
    >
      <template #reference>
        <el-button>点击弹出</el-button>
      </template>
      <el-table :data="gridData">
        <el-table-column property="date" label="Date" width="150"/>
        <el-table-column property="name" label="Name" width="100"/>
        <el-table-column property="address" label="Address"/>
      </el-table>
    </el-popover>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'

const popoverVisible = ref(false)

const gridData = [
  { date: '2016-05-02', name: 'Peter', address: 'No.1518, Jinshajiang Road, Putuo District' },
  { date: '2016-05-04', name: 'Tom', address: 'No.1518, Jinshajiang Road, Putuo District' },
  { date: '2016-05-01', name: 'Jerry', address: 'No.1518, Jinshajiang Road, Putuo District' },
  { date: '2016-05-03', name: 'Lucy', address: 'No.1518, Jinshajiang Road, Putuo District' },
]

const handleEsc = (e) => {
  if (e.key === 'Escape') {
    e.stopPropagation()
    popoverVisible.value = false
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleEsc, true)
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', handleEsc, true)
})
</script>

<template>
  <div class="document-management">
    <h1>文档管理</h1>
    <DocUpload />
    <div class="list">
      <h2>已上传文档</h2>
      <ul v-if="documents.length">
        <li v-for="doc in documents" :key="doc.id">
          <strong>{{ doc.name }}</strong>
          <span> - {{ doc.chunks }} 个片段 - {{ doc.status }}</span>
        </li>
      </ul>
      <p v-else>暂无文档，请先上传。</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import DocUpload from '../components/upload/DocUpload.vue'
import { useDocumentsStore } from '../store/documents'

const documentsStore = useDocumentsStore()
const documents = computed(() => documentsStore.documents)
</script>

<style scoped>
.document-management {
  padding: 20px;
}

h1 {
  color: #333;
}

.list {
  margin-top: 20px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin-bottom: 8px;
  color: #444;
}
</style>
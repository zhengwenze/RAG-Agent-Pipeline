<template>
  <div class="doc-upload">
    <h2>文档上传</h2>
    <input type="file" multiple @change="onFileChange" />
    <button :disabled="!files || loading" @click="handleUpload">
      {{ loading ? '上传中...' : '上传' }}
    </button>
    <p v-if="message" class="status">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useDocumentsStore } from '../../store/documents'
import { uploadDocumentsApi } from '../../api/client'

const documentsStore = useDocumentsStore()
const files = ref<FileList | null>(null)
const loading = ref(false)
const message = ref('')

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  files.value = target.files
}

const handleUpload = async () => {
  if (!files.value || loading.value) return
  loading.value = true
  message.value = ''
  try {
    const res = await uploadDocumentsApi(files.value)
    documentsStore.addDocument({
      id: Date.now(),
      name: files.value.item(0)?.name ?? '未命名文件',
      chunks: res.chunks,
      status: res.status,
    })
    message.value = `上传成功，切分为 ${res.chunks} 个片段`
  } catch (e: any) {
    message.value = e?.message || '上传失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.doc-upload {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
}

input[type='file'] {
  margin-bottom: 10px;
}

button {
  padding: 10px 20px;
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  opacity: 0.6;
  cursor: default;
}

button:hover:not(:disabled) {
  background-color: #0b7dda;
}

.status {
  margin-top: 10px;
  color: #555;
}
</style>
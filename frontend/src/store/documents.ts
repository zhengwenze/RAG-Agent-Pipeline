import { defineStore } from 'pinia'

export interface DocumentItem {
  id: number
  name: string
  chunks: number
  status: string
}

interface DocumentsState {
  documents: DocumentItem[]
}

export const useDocumentsStore = defineStore('documents', {
  state: (): DocumentsState => ({
    documents: [],
  }),
  actions: {
    addDocument(document: DocumentItem) {
      this.documents.push(document)
    },
    clear() {
      this.documents = []
    },
  },
})
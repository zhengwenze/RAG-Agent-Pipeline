import { defineStore } from 'pinia'

export const useDocumentsStore = defineStore('documents', {
  state: () => ({
    documents: []
  }),
  actions: {
    addDocument(document: any) {
      this.documents.push(document)
    }
  }
})
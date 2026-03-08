import { defineStore } from 'pinia'

export const useChatStore = defineStore('chat', {
  state: () => ({
    messages: []
  }),
  actions: {
    addMessage(message: any) {
      this.messages.push(message)
    }
  }
})
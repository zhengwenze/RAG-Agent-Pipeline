import { defineStore } from 'pinia'

export type ChatRole = 'user' | 'assistant'

export interface ChatMessage {
  id: number
  role: ChatRole
  text: string
}

interface ChatState {
  messages: ChatMessage[]
}

export const useChatStore = defineStore('chat', {
  state: (): ChatState => ({
    messages: [],
  }),
  actions: {
    addMessage(message: ChatMessage) {
      this.messages.push(message)
    },
    clear() {
      this.messages = []
    },
  },
})
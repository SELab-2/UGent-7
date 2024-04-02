import { ref } from 'vue'
import { type ToastMessageOptions } from 'primevue/toast'
import { defineStore } from 'pinia'

export const useMessagesStore = defineStore('messages', () => {
    /* State */
    const message = ref<ToastMessageOptions | null>(null)

    /**
     * Update the toast message.
     *
     * @param newMessage
     */
    function add(newMessage: ToastMessageOptions): void {
        message.value = newMessage
    }

    return {
        message,
        add
    }
})

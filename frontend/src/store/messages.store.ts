import { ref } from 'vue';
import { type ToastMessageOptions } from 'primevue/toast';
import { defineStore } from 'pinia';

export const useMessagesStore = defineStore('messages', () => {
    /* State */
    const message = ref<ToastMessageOptions | null>(null);

    /**
     * Add a success message to the toast.
     *
     * @param title
     * @param description
     * @returns void
     */
    function addSuccessMessage(title: string, description: string): void {
        message.value = {
            severity: 'success',
            summary: title,
            detail: description,
        };
    }

    /**
     * Add an error message to the toast.
     *
     * @param title
     * @param description
     */
    function addErrorMessage(title: string, description: string): void {
        message.value = {
            severity: 'error',
            summary: title,
            detail: description,
        };
    }

    /**
     * Add an info message to the toast.
     * @param title
     * @param description
     */
    function addInfoMessage(title: string, description: string): void {
        message.value = {
            severity: 'info',
            summary: title,
            detail: description,
        };
    }

    return {
        message,

        addSuccessMessage,
        addErrorMessage,
        addInfoMessage,
    };
});

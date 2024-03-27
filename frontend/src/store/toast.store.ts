import {ref} from 'vue';
import {ToastMessageOptions} from 'primevue/toast';
import {defineStore} from 'pinia';

export const useToastStore = defineStore('toast', {
    state: () => {
        return {
            message: ref<ToastMessageOptions|null>(null)
        }
    },
    actions: {
        /**
         * Update a toast message.
         *
         * @param message
         */
        add(message: ToastMessageOptions): void {
            this.message = message;
        }
    }
});
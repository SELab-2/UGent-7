<script setup lang="ts">
import Toast from 'primevue/toast';
import { watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useMessagesStore } from '@/store/messages.store.ts';
import { useToast } from 'primevue/usetoast';
import { storeToRefs } from 'pinia';

/* Composables */
const { t } = useI18n();
const { add } = useToast();
const { message } = storeToRefs(useMessagesStore());

/* Show a toast message when a new message is added */
watch(message, () => {
    // Check if the message is not null or undefined.
    if (message.value !== null) {
        // Check if the message has a detail.
        if (message.value.detail === null || message.value.detail === undefined) {
            message.value.detail = t('toasts.messages.unknown');
        }

        // Add the message to the toast.
        add({ ...message.value, life: 5000 });
    }
});
</script>

<template>
    <Toast />
    <RouterView />
</template>

<style lang="scss">
@import '@/main.scss';
</style>

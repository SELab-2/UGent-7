<script setup lang="ts">
import BaseLayout from '@/views/layout/base/BaseLayout.vue';
import Title from '@/views/layout/Title.vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/store/authentication.store.ts';
import { onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { useMessagesStore } from '@/store/messages.store.ts';

const { t } = useI18n();
const { query } = useRoute();
const { push } = useRouter();
const { login, intent } = useAuthStore();
const { addErrorMessage } = useMessagesStore();

onMounted(async () => {
    // Try catch block to catch any errors that might occur during the login process
    try {
        await login(query.ticket as string);
    } catch (error) {
        addErrorMessage(t('toasts.messages.error'), t('toasts.messages.login.error'));
    }
    await push(intent);
});
</script>

<template>
    <BaseLayout>
        <div class="w-8 mx-auto surface-100 p-4">
            <Title>{{ t('views.login.title') }}</Title>
            <div class="flex align-items-center mt-3">
                <span class="mr-2">{{ t('views.verify.redirect') }}</span>
                <span class="pi pi-spin pi-spinner" />
            </div>
        </div>
    </BaseLayout>
</template>

<style scoped lang="scss"></style>

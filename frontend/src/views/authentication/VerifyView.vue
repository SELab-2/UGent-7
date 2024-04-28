<script setup lang="ts">
import BaseLayout from '@/components/layout/base/BaseLayout.vue';
import Title from '@/components/layout/Title.vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/store/authentication.store.ts';
import { onMounted } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
const { query } = useRoute();
const { push } = useRouter();
const { login, intent } = useAuthStore();

onMounted(async () => {
    await login(query.ticket as string);
    await push(intent);
});
</script>

<template>
    <BaseLayout>
        <div class="w-8 mx-auto surface-100 p-4">
            <Title>Inloggen</Title>
            <div class="flex align-items-center mt-3">
                <span class="mr-2">{{ t('views.verify.redirect') }}</span>
                <span class="pi pi-spin pi-spinner" />
            </div>
        </div>
    </BaseLayout>
</template>

<style scoped lang="scss"></style>

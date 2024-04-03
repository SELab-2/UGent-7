<script setup lang="ts">
import Dropdown from 'primevue/dropdown';
import { storeToRefs } from 'pinia';
import { useAuthStore } from '@/store/authentication.store.ts';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
const { view, user } = storeToRefs(useAuthStore());
</script>

<template>
    <template v-if="user !== null">
        <Dropdown id="view" v-model="view" class="w-auto" :options="user.roles" variant="outlined">
            <template #option="{ option }">
                <div class="flex align-items-center">
                    <div>
                        {{ t('layout.header.view', [t('types.roles.' + option).toLowerCase()]) }}
                    </div>
                </div>
            </template>
            <template #value="{ value }">
                <div class="h-full flex justify-content-center align-items-center">
                    <div class="text-sm">{{ t('types.roles.' + value) }}</div>
                </div>
            </template>
        </Dropdown>
    </template>
</template>

<style scoped lang="scss"></style>

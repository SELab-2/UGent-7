<script setup lang="ts">
import Badge from 'primevue/badge';
import { PrimeIcons } from 'primevue/api';
import { useI18n } from 'vue-i18n';
import { type Notification } from '@/types/Notification.ts';

/* Props */
defineProps<{
    notification: Notification;
}>();

/* Composable injections */
const { t } = useI18n();
</script>

<template>
    <div class="flex flex-column border-bottom-1 border-300 py-2 gap-1">
        <!-- Header -->
        <div class="flex align-items-center gap-2">
            <i :class="PrimeIcons.BELL" />
            <b class="text-primary"
                >{{ notification.title }}
                <Badge
                    severity="secondary"
                    :value="t('layout.header.notifications.new')"
                    v-if="!notification.is_read"
                />
            </b>
        </div>
        <!-- Content -->
        <div>{{ notification.content }}</div>
        <!-- Date -->
        <div class="flex justify-content-end">
            {{ notification.getFormattedCreatedAt() }}
        </div>
    </div>
</template>

<style scoped lang="scss"></style>

<script setup lang="ts">
import ScrollPanel from 'primevue/scrollpanel';
import { type Notification } from '@/types/Notification.ts';
import NotificationCard from '@/components/notifications/NotificationCard.vue';
import { useI18n } from 'vue-i18n';

/* Props */
defineProps<{
    notifications: Notification[];
}>();

/* Composable injections */
const { t } = useI18n();
</script>

<template>
    <ScrollPanel class="border-1 border-200 p-2 h-25rem">
        <!-- Notification list -->
        <div class="flex flex-column gap-3">
            <!-- Single notification -->
            <template v-if="notifications.length > 0">
                <NotificationCard
                    :notification="notification"
                    v-for="notification in notifications"
                    :key="notification.id"
                />
            </template>
            <template v-else>
                {{ t('layout.header.notifications.noNotifications') }}
            </template>
        </div>
    </ScrollPanel>
</template>

<style scoped lang="scss"></style>

<script setup lang="ts">
import ScrollPanel from 'primevue/scrollpanel';
import { type Notification } from '@/types/Notification.ts';
import NotificationCard from '@/components/notifications/NotificationCard.vue';

/* Props */
defineProps<{
    notifications: Notification[];
}>();
</script>

<template>
    <ScrollPanel class="border-1 border-200 p-2 h-25rem">
        <!-- Notification list -->
        <div class="flex flex-column gap-3">
            <!-- Single notification -->
            <NotificationCard
                :notification="notification"
                v-for="notification in notifications"
                :key="notification.id"
            />
        </div>
    </ScrollPanel>
</template>

<style scoped lang="scss"></style>

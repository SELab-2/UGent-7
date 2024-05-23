<script setup lang="ts">
import NotificationsScrollPanel from '@/components/notifications/NotificationsScrollPanel.vue';
import Button from 'primevue/button';
import OverlayPanel from 'primevue/overlaypanel';
import Skeleton from 'primevue/skeleton';
import Badge from 'primevue/badge';
import { PrimeIcons } from 'primevue/api';
import { storeToRefs } from 'pinia';
import { useNotificationStore } from '@/store/notification.store.ts';
import { useI18n } from 'vue-i18n';
import { ref } from 'vue';

/* Composable injections */
const { t } = useI18n();
const { notifications, notificationCount, hasUnreadNotifications, unreadNotifications } =
    storeToRefs(useNotificationStore());
const { markNotificationsAsRead } = useNotificationStore();

/* State */
const notificationOverlay = ref();

/**
 * Toggles the notification overlay.
 */
function toggleNotificationOverlay(event: Event): void {
    notificationOverlay.value.toggle(event);
}
</script>

<template>
    <template v-if="unreadNotifications !== null">
        <div class="fadein">
            <Button
                class="text-xs"
                badge-severity="warning"
                :severity="hasUnreadNotifications ? 'secondary' : 'primary'"
                :badge="unreadNotifications.length.toString()"
                :icon="PrimeIcons.BELL"
                @click="toggleNotificationOverlay"
                rounded
            >
            </Button>
        </div>
        <template v-if="notifications !== null">
            <OverlayPanel ref="notificationOverlay">
                <div class="flex align-items-center gap-2 mb-2">
                    <h3>{{ t('layout.header.notifications.title') }}</h3>
                    <Badge :value="notifications.length.toString()" />
                </div>
                <NotificationsScrollPanel :notifications="notifications" />
                <div class="flex align-items-center gap-2 mt-4">
                    <Button
                        :label="t('layout.header.notifications.loadMore')"
                        @click="notificationCount += notificationCount"
                        link
                    />
                    <Button
                        class="ml-auto"
                        :label="t('layout.header.notifications.markAsRead')"
                        :disabled="!hasUnreadNotifications"
                        @click="markNotificationsAsRead"
                        outlined
                    />
                </div>
            </OverlayPanel>
        </template>
    </template>
    <template v-else>
        <Skeleton width="100px" height="42px" />
    </template>
</template>

<style scoped lang="scss"></style>

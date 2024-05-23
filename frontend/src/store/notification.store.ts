import { defineStore, storeToRefs } from 'pinia';
import { useAuthStore } from '@/store/authentication.store.ts';
import { useInterval, watchImmediate } from '@vueuse/core';
import { useNotifications } from '@/composables/services/notification.service.ts';
import { computed, ref } from 'vue';

export const useNotificationStore = defineStore('notification', () => {
    /* Composable injections */
    const { user } = storeToRefs(useAuthStore());
    const { notifications, getNotificationsByUser, readNotifications } = useNotifications();

    /* State */
    const notificationCounter = useInterval(300_000);
    const notificationCount = ref(5);

    /* Computed */
    const unreadNotifications = computed(() =>
        notifications.value !== null ? notifications.value.filter((n) => !n.is_read) : null,
    );

    const hasUnreadNotifications = computed<boolean>(() => {
        return unreadNotifications.value !== null && unreadNotifications.value.length > 0;
    });

    /**
     * Mark the notifications as read.
     */
    async function markNotificationsAsRead(): Promise<void> {
        if (unreadNotifications.value !== null) {
            if (user.value !== null) {
                void readNotifications(user.value.id);

                for (const notification of unreadNotifications.value) {
                    notification.is_read = true;
                }
            }
        }
    }

    watchImmediate([notificationCounter, user, notificationCount], async () => {
        if (user.value !== null) {
            await getNotificationsByUser(user.value.id, notificationCount.value);

            if (notifications.value !== null) {
                notificationCount.value = notifications.value.length;
            }
        }
    });

    return {
        notifications,
        notificationCount,
        unreadNotifications,
        hasUnreadNotifications,
        markNotificationsAsRead,
    };
});

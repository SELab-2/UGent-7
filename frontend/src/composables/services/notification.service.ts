import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { getList, patch } from '@/composables/services/helpers.ts';
import { Notification } from '@/types/Notification.ts';
import { type Response } from '@/types/Response.ts';

interface NotificationState {
    notifications: Ref<Notification[] | null>;
    getNotificationsByUser: (userId: string, count?: number) => Promise<void>;
    readNotifications: (userId: string) => Promise<void>;
}

export function useNotifications(): NotificationState {
    const notifications = ref<Notification[] | null>(null);
    const response = ref<Response | null>(null);

    /**
     * Get the notifications by user.
     *
     * @param userId
     * @param count
     */
    async function getNotificationsByUser(userId: string, count: number = 10): Promise<void> {
        const endpoint = endpoints.notifications.byUser.replace('{userId}', userId);
        await getList<Notification>(endpoint, notifications, Notification.fromJSON, true, {
            count,
        });
    }

    /**
     * Mark the notifications as read.
     */
    async function readNotifications(userId: string): Promise<void> {
        const endpoint = endpoints.notifications.byUser.replace('{userId}', userId);
        await patch(endpoint, notifications, response);
    }

    return {
        notifications,
        getNotificationsByUser,
        readNotifications,
    };
}

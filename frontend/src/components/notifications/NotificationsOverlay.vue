<script setup lang="ts">
import { PrimeIcons } from 'primevue/api';
import { storeToRefs } from 'pinia';
import { useNotificationStore } from '@/store/notification.store.ts';
import { useI18n } from 'vue-i18n';

/* Composable injections */
const { t, locale } = useI18n();
const { notifications, hasUnreadNotifications, unreadNotifications } = storeToRefs(useNotificationStore());
const { markNotificationsAsRead } = useNotificationStore();
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
                <h3 class="mb-4">{{ t('layout.header.notifications.title') }}</h3>
                <template v-if="notifications.length > 0">
                    <ScrollPanel class="border-1 border-200 p-2 h-25rem">
                        <!-- Notification list -->
                        <div class="flex flex-column gap-3">
                            <!-- Single notification -->
                            <div
                                class="flex flex-column border-bottom-1 border-300 py-2 gap-1"
                                v-for="notification in notifications"
                            >
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
                        </div>
                    </ScrollPanel>
                    <Button
                        class="ml-auto mt-4"
                        :label="t('layout.header.notifications.markAsRead')"
                        :disabled="!hasUnreadNotifications"
                        @click="markNotificationsAsRead"
                        outlined
                    />
                </template>
            </OverlayPanel>
        </template>
    </template>
    <template v-else>
        <Skeleton width="100px" height="42px" />
    </template>
</template>

<style scoped lang="scss">

</style>
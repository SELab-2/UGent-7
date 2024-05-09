import { type RouteLocationNormalized } from 'vue-router';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';
import { useMessagesStore } from '@/store/messages.store.ts';
import { i18n } from '@/config/i18n.ts';

export async function AuthenticationGuard(to: RouteLocationNormalized): Promise<{ name: string } | undefined> {
    const { t } = i18n.global;
    const { addErrorMessage } = useMessagesStore();
    const { refreshUser } = useAuthStore();
    const { intent, isAuthenticated } = storeToRefs(useAuthStore());

    console.log(to.name as string);
    if (!isAuthenticated.value && !['login', 'verify'].includes(to.name as string)) {
        try {
            await refreshUser();
        } catch (error: any) {
            const detail: string = error.response.data.detail.toString();

            if (to.name !== 'dashboard') {
                addErrorMessage(t('toasts.messages.error'), detail);
            }
        }

        if (!isAuthenticated.value) {
            intent.value = to.fullPath;
            return { name: 'login' };
        }
    }
}

import { type RouteLocationNormalized } from 'vue-router';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';

export async function AuthenticationGuard(to: RouteLocationNormalized): Promise<{ name: string } | undefined> {
    const { refresh } = useAuthStore();
    const { intent } = storeToRefs(useAuthStore());

    const { isAuthenticated } = storeToRefs(useAuthStore());

    if (!['login', 'verify'].includes(to.name as string)) {
        if (!isAuthenticated.value) {
            await refresh();

            if (!isAuthenticated.value) {
                intent.value = to.fullPath;
                return { name: 'login' };
            }
        }
    }
}

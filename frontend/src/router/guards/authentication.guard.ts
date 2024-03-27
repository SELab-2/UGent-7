import {RouteLocationNormalized} from 'vue-router';
import {useAuthStore} from '@/store/authentication.store.ts';
import {storeToRefs} from 'pinia';

export async function AuthenticationGuard(to: RouteLocationNormalized) {
    const { refresh, pushIntent } = useAuthStore();
    const { isAuthenticated} = storeToRefs(useAuthStore());

    if (!['login', 'verify'].includes(to.name as string)) {
        if (!isAuthenticated.value) {
            await refresh();

            if (!isAuthenticated.value) {
                pushIntent(to.fullPath);

                return { name: 'login' };
            }
        }
    }
}
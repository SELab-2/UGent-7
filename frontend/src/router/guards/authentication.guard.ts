import {NavigationGuardNext, RouteLocationNormalized} from 'vue-router';
import {useAuthStore} from '@/store/authentication.store.ts';
import {storeToRefs} from 'pinia';

export async function AuthenticationGuard(to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) {
    const { login, pushIntent, popIntent } = useAuthStore();
    const { isAuthenticated} = storeToRefs(useAuthStore());

    if (to.name !== 'login' && !isAuthenticated.value) {
        // Attempt to log in the user.
        await login(to.query.ticket as string);

        if (isAuthenticated.value) {
            return next(popIntent());
        }
    }

    if (!['login', 'verify'].includes(to.name as string) && !isAuthenticated.value) {
        // We should redirect to the login page if the user is not authenticated.
        pushIntent(from.fullPath);

        return next({ name: 'login' });
    }

    return next();
}
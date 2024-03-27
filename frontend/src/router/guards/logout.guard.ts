import {NavigationGuardNext, RouteLocationNormalized} from 'vue-router';
import {useAuthStore} from '@/store/authentication.store.ts';

export async function LogoutGuard(_1: RouteLocationNormalized, _2: RouteLocationNormalized, next: NavigationGuardNext) {
    await useAuthStore().logout();

    return next({ name: 'login' });
}
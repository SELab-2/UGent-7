import { type NavigationGuardNext, type RouteLocationNormalized } from 'vue-router';
import { useAuthStore } from '@/store/authentication.store.ts';

export async function LogoutGuard(_1: RouteLocationNormalized, _2: RouteLocationNormalized, next: NavigationGuardNext): Promise<void> {
    await useAuthStore().logout();

    next({ name: 'login' });
}

import { useAuthStore } from '@/store/authentication.store.ts';
import { type RouteLocationRaw } from 'vue-router';

export function AdminGuard(): boolean | RouteLocationRaw {
    const { user } = useAuthStore();
    if (user?.is_staff ?? false) {
        return true;
    }
    return 'dashboard';
}

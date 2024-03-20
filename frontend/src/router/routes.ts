import DashboardView from '@/views/dashboard/DashboardView.vue';
import {RouteRecordRaw} from 'vue-router';

export const routes: RouteRecordRaw[] = [
    { path: '/', component: DashboardView, name: 'dashboard' }
];
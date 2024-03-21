import DashboardView from '@/views/dashboard/DashboardView.vue';
import CourseView from '@/views/courses/CourseView.vue';
import LoginView from '@/views/authentication/LoginView.vue';
import {RouteRecordRaw} from 'vue-router';

export const routes: RouteRecordRaw[] = [
    { path: '/auth/', children: [
        { path: 'login', component: LoginView, name: 'login' },
    ]},
    { path: '/', component: DashboardView, name: 'dashboard' },
    { path: '/courses/', children: [
        { path: ':id', component: CourseView, name: 'course-view' }
    ]},
    { path: '/:pathMatch(.*)*', redirect: { name: 'dashboard' } }
];
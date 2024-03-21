import DashboardView from '@/views/dashboard/DashboardView.vue';
import {RouteRecordRaw} from 'vue-router';
import CourseView from '@/views/courses/CourseView.vue';

export const routes: RouteRecordRaw[] = [
    { path: '/', component: DashboardView, name: 'dashboard' },
    { path: '/courses', children: [
        { path: ':id', component: CourseView, name: 'course-view' }
    ]},
    { path: '/:pathMatch(.*)*', redirect: { name: 'dashboard' } }
];
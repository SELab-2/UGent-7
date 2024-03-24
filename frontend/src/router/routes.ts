import DashboardView from '@/views/dashboard/DashboardView.vue';
import CourseView from '@/views/courses/CourseView.vue';
import ProjectView from '@/views/projects/ProjectView.vue';
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
    { path: '/projects/', children: [
            { path: ':id', component: ProjectView, name: 'project-view' }
    ]},
    { path: '/:pathMatch(.*)*', redirect: { name: 'dashboard' } }
];
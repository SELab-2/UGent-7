import { RouteRecordRaw } from 'vue-router';
import DashboardView from '@/views/dashboard/DashboardView.vue';
import CourseView from '@/views/courses/CourseView.vue';
import Dummy from '@/components/Dummy.vue';

export const routes: RouteRecordRaw[] = [
    { path: '/', component: DashboardView, name: 'dashboard' },
    { path: '/courses', name: 'courses', children: [
        { path: ':id', component: CourseView, name: 'view' }
    ]},
    { path: '/login', component: Dummy, name: 'login' }
];


/**
 * Routes:
 * 
 * ### COURSES ###
 * /courses
 * /courses/create (teacher / admin)
 * /courses/id
 * /courses/id/edit
 * /courses/id/projects
 * /courses/id/projects/id
 * /courses/id/projects/create
 * /courses/id/projects/id/edit
 * /courses/id/projects/id/groups
 * /courses/id/projects/id/submit
 * 
 * ### USERS ###
 * /users (teacher /admin)
 * /users/students/
 * /users/students/id
 * /users/admins
 * /users/admins/id
 * /users/teachers
 * /users/teachers/id
 * /users/assistants
 * /users/assistants/id
 * /users/id (teacher / admin)
 * 
 * ### FACULTIES ###
 * /faculties (teacher / admin)
 * /faculties/create (teacher / admin)
 * 
 * ### NOTIFICATIONS ###
 * /notifications
 * /notifications/id
 * 
 * ### AUTHENTICATION ###
 * /login
 */
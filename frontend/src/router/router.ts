import { RouteRecordRaw, createWebHistory, createRouter } from 'vue-router';

import DashboardView from '@/views/dashboard/DashboardView.vue';
import CourseView from '@/views/courses/CourseView.vue';
import Dummy from '@/components/Dummy.vue';
import PageNotFound from '@/components/PageNotFound.vue';

const routes: RouteRecordRaw[] = [
    { path: '/', component: DashboardView, name: 'dashboard' },

    // Courses
    { path: '/courses', children: [
        { path: '', component: Dummy, name: 'courses' },
        { path: 'create', component: Dummy, name: 'course-create' },
        // Single course  
        { path: ':id', children: [
            { path: '', component: CourseView, name: 'course' },
            { path: 'edit', component: Dummy, name: 'course-edit' },
            // Projects
            { path: 'projects', children: [
                { path: '', component: Dummy, name: 'projects' },
                { path: 'create', component: Dummy, name: 'project-create' },
                // Single project
                { path: ':id', children: [
                    { path: '', component: Dummy, name: 'project' },
                    { path: 'edit', component: Dummy, name: 'project-edit' },
                    { path: 'groups', component: Dummy, name: 'project-groups' },
                    { path: 'submit', component: Dummy, name: 'project-submit' },
                ]}
            ]},
        ]}
    ]},

    // Users
    { path: '/users', children: [
        { path: ':id', component: Dummy, name: 'user' },
        { path: 'students', children: [
            { path: '', component: Dummy, name: 'students' },
            { path: ':id', component: Dummy, name: 'student' },
        ]},
        { path: 'admins', children: [
            { path: '', component: Dummy, name: 'admins' },
            { path: ':id', component: Dummy, name: 'admin' },
        ]},
        { path: 'teachers', children: [
            { path: '', component: Dummy, name: 'teachers' },
            { path: ':id', component: Dummy, name: 'teacher' },
        ]},
        { path: 'assistants', children: [
            { path: '', component: Dummy, name: 'assistants' },
            { path: ':id', component: Dummy, name: 'assistant' },
        ]},
    ]},

    // Faculties
    { path: '/faculties', component: Dummy, name: 'faculties' },
    { path: '/faculties/create', component: Dummy, name: 'faculty-create' },

    // Notifications
    { path: '/notifications', component: Dummy, name: 'notifications' },
    { path: '/notifications/:id', component: Dummy, name: 'notification' },

    // Authentication
    { path: '/login', component: Dummy, name: 'login' },

    // Page not found
    { path: '/:pathMatch(.*)*', name: 'page-not-found', component: PageNotFound },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router


/**
 * Routes:
 * 
 * ### COURSES ###
 * /courses
 * /courses/create (teacher / admin)
 * /courses/id
 * /courses/id/edit
 * /courses/id/projects
 * /courses/id/projects/create
 * /courses/id/projects/id
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
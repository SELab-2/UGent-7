import { RouteRecordRaw, createWebHistory, createRouter } from 'vue-router';

// import { useUserStore } from '@/stores/userStore';
// TODO: after pinia setup is done

import DashboardView from '@/views/dashboard/DashboardView.vue';
import CourseView from '@/views/courses/CourseView.vue';
import Dummy from '@/components/Dummy.vue';
import LoginView from '@/views/authentication/LoginView.vue';

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
        ]},
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
    { path: '/auth/', children: [
        { path: 'login', component: LoginView, name: 'login' },
    ]},

    // Page not found: redirect to dashboard
    { path: '/:pathMatch(.*)*', redirect: { name: 'dashboard' } }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
})

// TODO: once pinia store is setup, implement navigation guards
// Navigation guard example:
router.beforeEach((to, _) => {
    const isAdmin: boolean = false
    if (to.name === 'faculty-create') {
        if (!isAdmin) {
            return false
        }
    }
})


export default router

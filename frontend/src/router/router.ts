// import { useUserStore } from '@/stores/userStore';
// TODO: after pinia setup is done

import DashboardView from '@/views/dashboard/DashboardView.vue';
import CourseView from '@/views/courses/CourseView.vue';
import CreateCourseView from '@/views/courses/CreateCourseView.vue';
import Dummy from '@/components/Dummy.vue';
import LoginView from '@/views/authentication/LoginView.vue';
import CalendarView from '@/views/calendar/CalendarView.vue';
import VerifyView from '@/views/authentication/VerifyView.vue';
import { type RouteRecordRaw, createWebHistory, createRouter } from 'vue-router';
import { AuthenticationGuard } from '@/router/guards/authentication.guard.ts';
import { LogoutGuard } from '@/router/guards/logout.guard.ts';
import ProjectView from '@/views/projects/ProjectView.vue';
import CreateProjectView from '@/views/projects/CreateProjectView.vue';
import SearchCourseView from '@/views/courses/SearchCourseView.vue';
import SubmissionView from "@/views/submissions/submissionView.vue";
import SingleProjectView from "@/views/projects/SingleProjectView.vue";

const routes: RouteRecordRaw[] = [
    // Authentication
    {
        path: '/auth/',
        children: [
            { path: 'login', component: LoginView, name: 'login' },
            { path: 'verify', component: VerifyView, name: 'verify' },
            {
                path: 'logout',
                component: { beforeRouteEnter: LogoutGuard },
                name: 'logout',
            },
        ],
    },

    { path: '/', component: DashboardView, name: 'dashboard' },

    // Courses
    {
        path: '/courses',
        children: [
            { path: '', component: SearchCourseView, name: 'courses' },
            { path: 'create', component: CreateCourseView, name: 'course-create' },
            // Single course
            {
                path: ':courseId',
                children: [
                    { path: '', component: CourseView, name: 'course' },
                    { path: 'edit', component: Dummy, name: 'course-edit' },
                    // Projects
                    {
                        path: 'courseProjects',
                        children: [
                            { path: '', component: Dummy, name: 'courseProjects' },
                            { path: 'create', component: CreateProjectView, name: 'project-create' },
                            // Single project
                            {
                                path: ':projectId',
                                children: [
                                    { path: '', component: SingleProjectView, name: 'courseProject' },
                                    { path: 'edit', component: Dummy, name: 'project-edit' },
                                    { path: 'groups', component: Dummy, name: 'project-groups' },
                                    { path: 'submit', component: Dummy, name: 'project-submit' },
                                    { path: 'submission', component: SubmissionView, name: 'submission'}
                                ],
                            },
                        ],
                    },
                ],
            },
        ],
    },

    // Calendar
    { path: '/calendar', component: CalendarView, name: 'calendar' },

    // Projects
    { path: '/projects', component: ProjectView, name: 'projects' },

    // Users
    {
        path: '/users',
        children: [
            { path: ':id', component: Dummy, name: 'user' },
            {
                path: 'students',
                children: [
                    { path: '', component: Dummy, name: 'students' },
                    { path: ':id', component: Dummy, name: 'student' },
                ],
            },
            {
                path: 'admins',
                children: [
                    { path: '', component: Dummy, name: 'admins' },
                    { path: ':id', component: Dummy, name: 'admin' },
                ],
            },
            {
                path: 'teachers',
                children: [
                    { path: '', component: Dummy, name: 'teachers' },
                    { path: ':id', component: Dummy, name: 'teacher' },
                ],
            },
            {
                path: 'assistants',
                children: [
                    { path: '', component: Dummy, name: 'assistants' },
                    { path: ':id', component: Dummy, name: 'assistant' },
                ],
            },
        ],
    },

    // Faculties
    { path: '/faculties', component: Dummy, name: 'faculties' },
    { path: '/faculties/create', component: Dummy, name: 'faculty-create' },

    // Notifications
    { path: '/notifications', component: Dummy, name: 'notifications' },
    { path: '/notifications/:id', component: Dummy, name: 'notification' },

    // Authentication
    { path: '/auth/', children: [{ path: 'login', component: LoginView, name: 'login' }] },

    // Page not found: redirect to dashboard
    { path: '/:pathMatch(.*)*', redirect: { name: 'dashboard' } },
];

const router = createRouter({
    history: createWebHistory(),
    linkActiveClass: 'active',
    routes,
});

router.beforeEach(AuthenticationGuard);

export default router;

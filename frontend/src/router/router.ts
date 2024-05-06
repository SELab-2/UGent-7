// import { useUserStore } from '@/stores/userStore';
// TODO: after pinia setup is done

import DashboardView from '@/views/dashboard/DashboardView.vue';
import HelpDashboard from '@/views/help/HelpDashboard.vue';
import CourseView from '@/views/courses/CourseView.vue';
import CreateCourseView from '@/views/courses/CreateCourseView.vue';
import UpdateCourseView from '@/views/courses/UpdateCourseView.vue';
import Dummy from '@/components/Dummy.vue';
import LoginView from '@/views/authentication/LoginView.vue';
import CalendarView from '@/views/calendar/CalendarView.vue';
import VerifyView from '@/views/authentication/VerifyView.vue';
import { type RouteRecordRaw, createWebHistory, createRouter } from 'vue-router';
import { AuthenticationGuard } from '@/router/guards/authentication.guard.ts';
import { LogoutGuard } from '@/router/guards/logout.guard.ts';
import { AdminGuard } from '@/router/guards/admin.guard.ts';
import ProjectView from '@/views/projects/ProjectView.vue';
import CreateProjectView from '@/views/projects/CreateProjectView.vue';
import UpdateProjectView from '@/views/projects/UpdateProjectView.vue';
import SearchCourseView from '@/views/courses/SearchCourseView.vue';
import SubmissionView from '@/views/submissions/SubmissionView.vue';
import AdminView from '@/views/admin/AdminView.vue';
import UsersView from '@/views/admin/UsersView.vue';
import ProjectsView from '@/views/projects/ProjectsView.vue';
import SubmissionsView from "@/views/submissions/SubmissionsView.vue";
import DockerImagesView from "@/views/admin/DockerImagesView.vue";
import JoinCourseView from '@/views/courses/JoinCourseView.vue';

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
                    { path: 'edit', component: UpdateCourseView, name: 'course-edit' },
                    {
                        path: 'join',
                        children: [{ path: ':invitationLink', component: JoinCourseView, name: 'course-join' }],
                    },
                    // Projects
                    {
                        path: 'projects',
                        children: [
                            { path: '', component: Dummy, name: 'course-projects' },
                            { path: 'create', component: CreateProjectView, name: 'project-create' },
                            // Single project
                            {
                                path: ':projectId',
                                children: [
                                    { path: '', component: ProjectView, name: 'course-project' },
                                    { path: 'edit', component: UpdateProjectView, name: 'project-edit' },
                                    {
                                        path: 'group',
                                        children: [
                                            { path: '', component: Dummy, name: 'group' },
                                            {
                                                path: ':groupId',
                                                children: [
                                                    { path: '', component: Dummy, name: 'project-group' },
                                                    {
                                                        path: 'submissions',
                                                        children: [
                                                            {
                                                                path: '',
                                                                component: SubmissionsView,
                                                                name: 'submissions',
                                                            },
                                                            {
                                                                path: ':submissionId',
                                                                children: [
                                                                    {
                                                                        path: '',
                                                                        component: SubmissionView,
                                                                        name: 'submission',
                                                                    },
                                                                ],
                                                            },
                                                        ],
                                                    },
                                                ],
                                            },
                                        ],
                                    },
                                    { path: 'groups', component: Dummy, name: 'project-groups' },
                                    { path: 'submit', component: Dummy, name: 'project-submit' },
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
    { path: '/projects', component: ProjectsView, name: 'projects' },

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

    // Admin
    {
        path: '/admin/',
        beforeEnter: AdminGuard,
        children: [
            { path: '', component: AdminView, name: 'admin' },
            { path: 'users', component: UsersView, name: 'admin-users' },
            { path: 'docker-images', component: DockerImagesView, name: 'admin-dockerImages' },
        ],
    },

    // help
    {
        path: '/help',
        children: [
            {
                path: '',
                component: HelpDashboard,
                name: 'help-dashboard',
            },
            {
                path: 'student',
                component: Dummy,
                name: 'help-student',
                children: [
                    {
                        path: 'login-out',
                        component: Dummy,
                        name: 'help-student-login_out',
                    },
                    {
                        path: 'change-lang',
                        component: Dummy,
                        name: 'help-student-change_lang',
                    },
                ],
            },
            {
                path: 'teacher',
                component: Dummy,
                name: 'help-teacher',
            },
            {
                path: 'assistant',
                component: Dummy,
                name: 'help-assistant',
            },
            {
                path: 'admin',
                component: Dummy,
                name: 'help-admin',
            },
        ],
    },

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

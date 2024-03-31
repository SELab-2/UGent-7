import axios from 'axios';
import {defineStore} from 'pinia';
import {Role, User} from '@/types/User.ts';
import {endpoints} from '@/config/endpoints.ts';
import {useMessagesStore} from '@/store/messages.store.ts';
import {client} from '@/composables/axios.ts';
import {Teacher} from '@/types/Teacher.ts';
import {Student} from '@/types/Student.ts';
import {Assistant} from '@/types/Assistant.ts';
import {useLocalStorage} from '@vueuse/core';
import { useCourses } from '@/composables/services/courses.service';
import {computed, ref, watch} from 'vue';

export const useAuthStore = defineStore('auth', () => {
    /* Stores */
    const user = ref<User|null>(null);
    const view = useLocalStorage<Role|null>('view', null);
    const intent = useLocalStorage<string>('intent', '/');

    /* Services */
    const { courses, getCoursesByTeacher, getCoursesByStudent, getCourseByAssistant } = useCourses();

    /* Update the user object when the view changes. */
    watch(view, async () => {
        initUser();
    });

    const initUser = async () => {
        if (user.value !== null) {
            if (view.value === 'teacher') {
                await getCoursesByTeacher(user.value.id);

                user.value = new Teacher(
                    user.value.id,
                    user.value.username,
                    user.value.email,
                    user.value.first_name,
                    user.value.last_name,
                    user.value.last_enrolled,
                    user.value.is_staff,
                    user.value.roles,
                    [],
                    courses.value ?? [],
                    user.value.create_time,
                    user.value.last_login
                );
            }else if (view.value === 'student') {
                await getCoursesByStudent(user.value.id);

                user.value = new Student(
                    user.value.id,
                    user.value.username,
                    user.value.email,
                    user.value.first_name,
                    user.value.last_name,
                    user.value.is_staff,
                    user.value.last_enrolled,
                    user.value.create_time,
                    user.value.last_login,
                    user.value.id,
                    user.value.roles,
                    courses.value ?? []
                );
            }else {
                await getCourseByAssistant(user.value.id);

                user.value = new Assistant(
                    user.value.id,
                    user.value.username,
                    user.value.email,
                    user.value.first_name,
                    user.value.last_name,
                    user.value.last_enrolled,
                    user.value.is_staff,
                    user.value.roles,
                    [],
                    courses.value ?? [],
                    user.value.create_time,
                    user.value.last_login
                );
            }
        }
    };


    /**
     * Attempt to log in the user using a CAS ticket.
     *
     * @param ticket
     */
    async function login(ticket: string) {
        // Display toast messages.
        const { add } = useMessagesStore();

        // Attempt to log in the user using the ticket.
        await axios.post(endpoints.auth.token.obtain, {
            ticket
        }).then(() => {
            add({
                severity: 'success',
                summary: 'Success',
                detail: 'You have successfully logged in.'
            })
        }).catch((error) => {
            add({
                severity: 'error',
                summary: error.response.statusText,
                detail: error.response.data.detail
            });
        });
    }

    /**
     * Refresh the user objects in the API endpoint.
     */
    async function refresh() {
        // Display toast messages.
        const { add } = useMessagesStore();

        // Get the user information (using a cookie).
        await axios.get(endpoints.auth.whoami).then(response => {
            user.value = User.fromJSON(response.data);

            if (view.value === null) {
                view.value = user.value.roles[0];
            }

            // Init the user depending on the role selected.
            initUser();

        }).catch((error) => {
            add({
                severity: 'error',
                summary: error.response.statusText,
                detail: error.response.data.detail
            });
        });
    }

    /**
     * Log out the user.
     */
    async function logout() {
        await client.post(endpoints.auth.logout).catch();
        user.value = null;
    }

    /* Getters */
    const isAuthenticated = computed(() => {
        return user.value !== null;
    });

    return {
        user, view, intent,
        login, refresh, logout,
        isAuthenticated
    }
});
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
import {computed, ref} from 'vue';

export const useAuthStore = defineStore('auth', () => {
    /* Stores */
    const user = ref<User|null>(null);
    const teacher = ref<Teacher|null>(null);
    const student = ref<Student|null>(null);
    const assistant = ref<Assistant|null>(null);
    const view = useLocalStorage<Role|null>('view', null);
    const intent = useLocalStorage<string>('intent', '/');

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

            // TODO: Get the teacher, student, and assistant information.

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
        user, teacher, student, assistant, view, intent,
        login, refresh, logout,
        isAuthenticated
    }
});
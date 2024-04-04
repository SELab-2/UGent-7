import axios from 'axios';
import { defineStore } from 'pinia';
import { type Role, User } from '@/types/users/User.ts';
import { endpoints } from '@/config/endpoints.ts';
import { useMessagesStore } from '@/store/messages.store.ts';
import { client } from '@/config/axios.ts';
import { useLocalStorage } from '@vueuse/core';
import { computed, ref, watch } from 'vue';
import { useAssistant } from '@/composables/services/assistant.service';
import { useStudents } from '@/composables/services/students.service';
import { useTeacher } from '@/composables/services/teachers.service';
import { type Teacher } from '@/types/users/Teacher.ts';
import { type Student } from '@/types/users/Student.ts';
import { type Assistant } from '@/types/users/Assistant.ts';
import { useI18n } from 'vue-i18n';

export const useAuthStore = defineStore('auth', () => {
    /* Stores */
    const user = ref<User | Teacher | Student | Assistant | null>(null);
    const view = useLocalStorage<Role | null>('view', null);
    const intent = useLocalStorage<string>('intent', '/');

    /* Services */
    const { assistant, getAssistantByID } = useAssistant();
    const { student, getStudentByID } = useStudents();
    const { teacher, getTeacherByID } = useTeacher();

    /* Update the user object when the view changes. */
    watch(view, async () => {
        await initUser();
    });

    /**
     * Initialize the user object depending on the role.
     */
    async function initUser(): Promise<void> {
        if (user.value !== null) {
            if (view.value === 'teacher') {
                // Get the teacher information.
                await getTeacherByID(user.value.id, true);

                // Set the user object with the teacher information.
                if (teacher.value !== undefined && teacher.value !== null) {
                    teacher.value.roles = user.value.roles;
                }

                user.value = teacher.value;
            } else if (view.value === 'student') {
                // Get the student information.
                await getStudentByID(user.value.id, true);

                // Set the user object with the student information.
                if (student.value !== undefined && student.value !== null) {
                    student.value.roles = user.value.roles;
                }

                user.value = student.value;
            } else {
                // Get the assistant information.
                await getAssistantByID(user.value.id, true);

                // Set the user object with the assistant information.
                if (assistant.value !== undefined && assistant.value !== null) {
                    assistant.value.roles = user.value.roles;
                }

                user.value = assistant.value;
            }
        }
    }

    /**
     * Refresh the user objects in the API endpoint.
     */
    async function refreshUser(): Promise<void> {
        // Display toast messages.
        const { addErrorMessage } = useMessagesStore();

        // Get the user information (using a cookie).
        try {
            // Get the user information when it is not set.
            if (user.value === null) {
                const response = await axios.get(endpoints.auth.whoami);
                user.value = User.fromJSON(response.data as User);
            }

            if (view.value === null) {
                view.value = user.value.roles[0];
            }

            // Get the role information.
            await initUser();
        } catch (error: any) {
            addErrorMessage(
                error.response.statusText as string,
                error.response.data.detail as string,
            );
        }
    }

    /**
     * Attempt to log in the user using a CAS ticket.
     *
     * @param ticket
     */
    async function login(ticket: string): Promise<void> {
        // Display toast messages.
        const { t } = useI18n();
        const { addSuccessMessage, addErrorMessage } = useMessagesStore();

        // Attempt to log in the user using the ticket.
        try {
            await axios.post(endpoints.auth.token.obtain, {
                ticket,
            });

            addSuccessMessage(
                t('toasts.messages.success'),
                t('toasts.messages.login.success'),
            );
        } catch (error: any) {
            addErrorMessage(
                t('toasts.messages.error'),
                error.response.data.detail as string,
            );
        }
    }

    /**
     * Log out the user.
     */
    async function logout(): Promise<void> {
        await client.post(endpoints.auth.logout);
        user.value = null;
    }

    /* Getters */
    const isAuthenticated = computed(() => {
        return user.value !== null;
    });

    return {
        user,
        student,
        teacher,
        assistant,
        view,
        intent,
        login,
        refreshUser,
        logout,
        isAuthenticated,
    };
});

import axios from 'axios'
import { defineStore } from 'pinia'
import { type Role, User } from '@/types/User.ts'
import { endpoints } from '@/config/endpoints.ts'
import { useMessagesStore } from '@/store/messages.store.ts'
import { client } from '@/composables/axios.ts'
import { useLocalStorage } from '@vueuse/core'
import { useCourses } from '@/composables/services/courses.service'
import { computed, ref, watch } from 'vue'
import { useAssistant } from '@/composables/services/assistant.service'
import { useStudents } from '@/composables/services/students.service'
import { useTeacher } from '@/composables/services/teachers.service'

export const useAuthStore = defineStore('auth', () => {
    /* Stores */
    const user = ref<User | null>(null)
    const view = useLocalStorage<Role | null>('view', null)
    const intent = useLocalStorage<string>('intent', '/')

    /* Services */
    const {
        courses,
        getCoursesByTeacher,
        getCoursesByStudent,
        getCourseByAssistant
    } = useCourses()
    const { assistant, getAssistantByID } = useAssistant()
    const { student, getStudentByID } = useStudents()
    const { teacher, getTeacherByID } = useTeacher()

    /* Update the user object when the view changes. */
    watch(view, async () => {
        initUser()
    })

    const initUser = async () => {
        if (user.value !== null) {
            if (view.value === 'teacher') {
                // Get the teacher information.
                await getTeacherByID(user.value.id)

                // Get the courses for the teacher.
                await getCoursesByTeacher(user.value.id)

                // Set the user object with the teacher information.
                if (teacher.value !== undefined && teacher.value !== null) {
                    teacher.value.courses = courses.value ?? []
                    teacher.value.roles = user.value.roles
                }

                user.value = teacher.value
            } else if (view.value === 'student') {
                // Get the student information.
                await getStudentByID(user.value.id)

                // Get the courses for the student.
                await getCoursesByStudent(user.value.id)

                // Set the user object with the student information.
                if (student.value !== undefined && student.value !== null) {
                    student.value.courses = courses.value ?? []
                    student.value.roles = user.value.roles
                }

                user.value = student.value
            } else {
                // Get the assistant information.
                await getAssistantByID(user.value.id)

                // Get the courses for the assistant.
                await getCourseByAssistant(user.value.id)

                // Set the user object with the assistant information.
                if (assistant.value !== undefined && assistant.value !== null) {
                    assistant.value.courses = courses.value ?? []
                    assistant.value.roles = user.value.roles
                }

                user.value = assistant.value
            }
        }
    }

    /**
     * Attempt to log in the user using a CAS ticket.
     *
     * @param ticket
     */
    async function login(ticket: string) {
        // Display toast messages.
        const { add } = useMessagesStore()

        // Attempt to log in the user using the ticket.
        await axios
            .post(endpoints.auth.token.obtain, {
                ticket
            })
            .then(() => {
                add({
                    severity: 'success',
                    summary: 'Success',
                    detail: 'You have successfully logged in.'
                })
            })
            .catch((error) => {
                add({
                    severity: 'error',
                    summary: error.response.statusText,
                    detail: error.response.data.detail
                })
            })
    }

    /**
     * Refresh the user objects in the API endpoint.
     */
    async function refresh() {
        // Display toast messages.
        const { add } = useMessagesStore()

        // Get the user information (using a cookie).
        await axios
            .get(endpoints.auth.whoami)
            .then((response) => {
                user.value = User.fromJSON(response.data as User)

                if (view.value === null) {
                    view.value = user.value.roles[0]
                }

                // Init the user depending on the role selected.
                initUser()
            })
            .catch((error) => {
                add({
                    severity: 'error',
                    summary: error.response.statusText,
                    detail: error.response.data.detail
                })
            })
    }

    /**
     * Log out the user.
     */
    async function logout() {
        await client.post(endpoints.auth.logout).catch()
        user.value = null
    }

    /* Getters */
    const isAuthenticated = computed(() => {
        return user.value !== null
    })

    return {
        user,
        view,
        intent,
        login,
        refresh,
        logout,
        isAuthenticated
    }
})

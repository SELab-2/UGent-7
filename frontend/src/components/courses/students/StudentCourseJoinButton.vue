<script setup lang="ts">
import Button from 'primevue/button';
import { Course } from '@/types/Course.ts';
import { Student } from '@/types/users/Student.ts';
import { useAuthStore } from '@/store/authentication.store.ts';
import { useMessagesStore } from '@/store/messages.store.ts';
import { useStudents } from '@/composables/services/students.service.ts';
import { useI18n } from 'vue-i18n';

/* Props */
const props = defineProps<{student: Student, course: Course}>();

/* Composable injections */
const { refreshUser } = useAuthStore();
const { addSuccessMessage, addErrorMessage } = useMessagesStore();
const { studentJoinCourse, studentLeaveCourse } = useStudents();
const { t } = useI18n();

/**
 * Enroll the student in the course.
 */
function joinCourse(): void {
    studentJoinCourse(props.course.id, props.student.id).then(() => {
        addSuccessMessage(
            t('toasts.messages.success'),
            t('toasts.messages.courses.enrollment.success', [props.course.name])
        );

        refreshUser();
    }).catch(() => {
        addErrorMessage(
            t('toasts.messages.error'),
            t('toasts.messages.courses.enrollment.error', [props.course.name])
        );
    });
}

/**
 * Leave the course.
 */
function leaveCourse(): void {
    studentLeaveCourse(props.course.id, props.student.id).then(() => {
        addSuccessMessage(
            t('toasts.messages.success'),
            t('toasts.messages.courses.leave.success', [props.course.name])
        );
        refreshUser();
    }).catch(() => {
        addErrorMessage(
            t('toasts.messages.error'),
            t('toasts.messages.courses.leave.error', [props.course.name])
        );
    });
}
</script>

<template>
    <Button
        class="text-sm p-0"
        label="Inschrijven"
        icon-pos="right"
        icon="pi pi-arrow-right"
        @click="joinCourse"
        v-if="!student.hasCourse(course)"
        link />
    <Button
        class="text-sm p-0"
        label="Uitschrijven"
        icon-pos="right"
        icon="pi pi-arrow-right"
        @click="leaveCourse"
        v-else
        link />
</template>

<style scoped lang="scss">

</style>
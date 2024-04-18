<script setup lang="ts">
import Button from 'primevue/button';
import { type Course } from '@/types/Course.ts';
import { type Student } from '@/types/users/Student.ts';
import { useMessagesStore } from '@/store/messages.store.ts';
import { useStudents } from '@/composables/services/student.service.ts';
import { useI18n } from 'vue-i18n';

/* Props */
const props = defineProps<{ student: Student; courses: Course[]; course: Course }>();

/* Composable injections */
const { addSuccessMessage, addErrorMessage } = useMessagesStore();
const { studentJoinCourse, studentLeaveCourse } = useStudents();
const { t } = useI18n();

/* Emits */
const emit = defineEmits(['update:courses']);

/**
 * Check if the student has already enrolled in the course.
 *
 * @param course The course to check
 * @returns True if the student has the course, false otherwise
 */
function hasCourse(course: Course): boolean {
    return props.courses.some((c) => c.id === course.id);
}

/**
 * Enroll the student in the course.
 */
async function joinCourse(): Promise<void> {
    try {
        await studentJoinCourse(props.course.id, props.student.id);

        addSuccessMessage(
            t('toasts.messages.success'),
            t('toasts.messages.courses.enrollment.success', [props.course.name]),
        );

        emit('update:courses');
    } catch (error) {
        addErrorMessage(t('toasts.messages.error'), t('toasts.messages.courses.enrollment.error', [props.course.name]));
    }
}

/**
 * Leave the course.
 */
async function leaveCourse(): Promise<void> {
    try {
        await studentLeaveCourse(props.course.id, props.student.id);

        addSuccessMessage(
            t('toasts.messages.success'),
            t('toasts.messages.courses.leave.success', [props.course.name]),
        );

        emit('update:courses');
    } catch (error) {
        addErrorMessage(t('toasts.messages.error'), t('toasts.messages.courses.leave.error', [props.course.name]));
    }
}
</script>

<template>
    <Button
        class="text-sm p-0"
        :label="t('views.courses.enroll')"
        icon-pos="right"
        icon="pi pi-arrow-right"
        @click="joinCourse"
        v-if="!hasCourse(course)"
        link
    />
    <Button
        class="text-sm p-0"
        :label="t('views.courses.leave')"
        icon-pos="right"
        icon="pi pi-arrow-right"
        @click="leaveCourse"
        v-else
        link
    />
</template>

<style scoped lang="scss"></style>

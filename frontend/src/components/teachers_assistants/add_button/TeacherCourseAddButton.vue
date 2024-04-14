<script setup lang="ts">
import Button from 'primevue/button';
import { type Course } from '@/types/Course.ts';
import { type User } from '@/types/users/User.ts';
import { type Teacher } from '@/types/users/Teacher';
import { useMessagesStore } from '@/store/messages.store.ts';
import { useI18n } from 'vue-i18n';
import { useTeacher } from '@/composables/services/teachers.service';
import { ref } from 'vue';

/* Props */
const props = defineProps<{ user: User; course: Course }>();

/* Composable injections */
const { addSuccessMessage, addErrorMessage } = useMessagesStore();
const { teachers, teacherJoinCourse, teacherLeaveCourse, getTeacherByCourse } = useTeacher();
const { t } = useI18n();

/* State */
const courseValue = ref<Course>(props.course);

/**
 * Enroll the user in the course.
 */
async function joinCourse(): Promise<void> {
    try {
        await teacherJoinCourse(courseValue.value.id, props.user.id);

        addSuccessMessage(
            t('toasts.messages.success'),
            t('toasts.messages.courses.teachers_and_assistants.enroll.success', [
                props.user.getFullName(),
                t('types.roles.teacher'),
            ]),
        );

        await refreshCourse();
    } catch (error) {
        addErrorMessage(
            t('toasts.messages.error'),
            t('toasts.messages.courses.teachers_and_assistants.enroll.error', [
                props.user.getFullName(),
                t('types.roles.teacher'),
            ]),
        );
    }
}

/**
 * Leave the course.
 */
async function leaveCourse(): Promise<void> {
    try {
        await teacherLeaveCourse(courseValue.value.id, props.user.id);

        addSuccessMessage(
            t('toasts.messages.success'),
            t('toasts.messages.courses.teachers_and_assistants.leave.success', [props.user.getFullName()]),
        );

        await refreshCourse();
    } catch (error) {
        addErrorMessage(
            t('toasts.messages.error'),
            t('toasts.messages.courses.teachers_and_assistants.leave.error', [props.user.getFullName()]),
        );
    }
}

/* Refreshes the course data by updating the teachers */
async function refreshCourse(): Promise<void> {
    await getTeacherByCourse(props.course.id);
    courseValue.value.teachers = teachers.value ?? [];
}
</script>

<template>
    <Button
        class="text-sm p-0 custom-button"
        :label="t('views.courses.teachers_and_assistants.enroll', [t('types.roles.teacher')])"
        icon-pos="right"
        icon="pi pi-arrow-right"
        @click="joinCourse"
        v-if="!courseValue.hasTeacher(user as Teacher)"
        link
    />
    <Button
        class="text-sm p-0 custom-button"
        :label="t('views.courses.teachers_and_assistants.leave')"
        icon-pos="right"
        icon="pi pi-arrow-right"
        @click="leaveCourse"
        v-else
        link
    />
</template>

<style scoped lang="scss">
.custom-button {
    display: flex;
    justify-content: flex-start;
    text-align: left;
}
</style>

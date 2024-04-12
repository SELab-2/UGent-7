<script setup lang="ts">
import Button from 'primevue/button';
import { type Course } from '@/types/Course.ts';
import { type User } from '@/types/users/User.ts';
import { type Assistant } from '@/types/users/Assistant';
import { type Teacher } from '@/types/users/Teacher';
import { useAuthStore } from '@/store/authentication.store.ts';
import { useMessagesStore } from '@/store/messages.store.ts';
import { useI18n } from 'vue-i18n';
import { useAssistant } from '@/composables/services/assistant.service';
import { useTeacher } from '@/composables/services/teachers.service';

/* Props */
const props = defineProps<{ user: User; course: Course }>();

/* Composable injections */
const { refreshUser } = useAuthStore();
const { addSuccessMessage, addErrorMessage } = useMessagesStore();
const { assistantJoinCourse, assistantLeaveCourse } = useAssistant();
const { teacherJoinCourse, teacherLeaveCourse } = useTeacher();
const { t } = useI18n();

/**
 * Enroll the user in the course.
 */
async function joinCourse(): Promise<void> {
    try {
        if (props.user.isAssistant()) {
            const assistant = props.user as Assistant;
            await assistantJoinCourse(assistant.id, props.course.id);
        } else if (props.user.isTeacher()) {
            const teacher = props.user as Teacher;
            await teacherJoinCourse(teacher.id, props.course.id);
        }

        addSuccessMessage(
            t('toasts.messages.success'),
            t('toasts.messages.courses.enrollment.success', [props.course.name]),
        );

        // TODO:
        await refreshUser();
    } catch (error) {
        addErrorMessage(t('toasts.messages.error'), t('toasts.messages.courses.enrollment.error', [props.course.name]));
    }
}

/**
 * Leave the course.
 */
async function leaveCourse(): Promise<void> {
    try {
        if (props.user.isAssistant()) {
            const assistant = props.user as Assistant;
            await assistantLeaveCourse(assistant.id, props.course.id);
        } else if (props.user.isTeacher()) {
            const teacher = props.user as Teacher;
            await teacherLeaveCourse(teacher.id, props.course.id);
        }

        addSuccessMessage(
            t('toasts.messages.success'),
            t('toasts.messages.courses.leave.success', [props.course.name]),
        );

        // TODO:
        await refreshUser();
    } catch (error) {
        addErrorMessage(t('toasts.messages.error'), t('toasts.messages.courses.leave.error', [props.course.name]));
    }
}
</script>

<template>
    <Button
        class="text-sm p-0"
        label="Inschrijven"
        icon-pos="right"
        icon="pi pi-arrow-right"
        @click="joinCourse"
        v-if="(user.isAssistant() && ! course.hasAssistant(user as Assistant)) || (user.isTeacher() && ! course.hasTeacher(user as Teacher))"
        link
    />
    <Button
        class="text-sm p-0"
        label="Uitschrijven"
        icon-pos="right"
        icon="pi pi-arrow-right"
        @click="leaveCourse"
        v-else
        link
    />
</template>

<style scoped lang="scss"></style>

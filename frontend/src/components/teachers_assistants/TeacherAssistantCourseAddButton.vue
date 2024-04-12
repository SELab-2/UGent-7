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
            await assistantJoinCourse(props.course.id, props.user.id);
        } else if (props.user.isTeacher()) {
            await teacherJoinCourse(props.course.id, props.user.id);
        }

        addSuccessMessage(
            t('toasts.messages.success'),
            t('toasts.messages.courses.enrollment.success', [props.course.name]),
        );

        // TODO:
        // await refreshUser();
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
            await assistantLeaveCourse(props.course.id, props.user.id);
        } else if (props.user.isTeacher()) {
            await teacherLeaveCourse(props.course.id, props.user.id);
        }

        addSuccessMessage(
            t('toasts.messages.success'),
            t('toasts.messages.courses.leave.success', [props.course.name]),
        );

        // TODO:
        // await refreshUser();
    } catch (error) {
        addErrorMessage(t('toasts.messages.error'), t('toasts.messages.courses.leave.error', [props.course.name]));
    }
}
</script>

<template>
    <Button
        class="text-sm p-0 custom-button"
        :label="t('views.courses.teachers_and_assistants.enroll', [user.isAssistant() ? t('types.roles.assistant') : t('types.roles.teacher')])"
        icon-pos="right"
        icon="pi pi-arrow-right"
        @click="joinCourse"
        v-if="(user.isAssistant() && ! course.hasAssistant(user as Assistant)) || (user.isTeacher() && ! course.hasTeacher(user as Teacher))"
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

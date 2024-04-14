<script setup lang="ts">
import Button from 'primevue/button';
import { type Course } from '@/types/Course.ts';
import { type User } from '@/types/users/User.ts';
import { type Assistant } from '@/types/users/Assistant';
import { useMessagesStore } from '@/store/messages.store.ts';
import { useI18n } from 'vue-i18n';
import { useAssistant } from '@/composables/services/assistant.service';
import { ref } from 'vue';

/* Props */
const props = defineProps<{ user: User; course: Course }>();

/* Composable injections */
const { addSuccessMessage, addErrorMessage } = useMessagesStore();
const { assistants, assistantJoinCourse, assistantLeaveCourse, getAssistantByCourse } = useAssistant();
const { t } = useI18n();

/* State */
const courseValue = ref<Course>(props.course);

/**
 * Enroll the user in the course.
 */
async function joinCourse(): Promise<void> {
    try {
        await assistantJoinCourse(courseValue.value.id, props.user.id);

        addSuccessMessage(
            t('toasts.messages.success'),
            t('toasts.messages.courses.teachers_and_assistants.enroll.success', [
                props.user.getFullName(),
                t('types.roles.assistant'),
            ]),
        );

        await refreshCourse();
    } catch (error) {
        addErrorMessage(
            t('toasts.messages.error'),
            t('toasts.messages.courses.teachers_and_assistants.enroll.error', [
                props.user.getFullName(),
                t('types.roles.assistant'),
            ]),
        );
    }
}

/**
 * Leave the course.
 */
async function leaveCourse(): Promise<void> {
    try {
        await assistantLeaveCourse(courseValue.value.id, props.user.id);

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

/* Refreshes the course data by updating the assistants */
async function refreshCourse(): Promise<void> {
    await getAssistantByCourse(courseValue.value.id);
    courseValue.value.assistants = assistants.value ?? [];
}
</script>

<template>
    <Button
        class="text-sm p-0 custom-button"
        :label="t('views.courses.teachers_and_assistants.enroll', [t('types.roles.assistant')])"
        icon-pos="right"
        icon="pi pi-arrow-right"
        @click="joinCourse"
        v-if="!courseValue.hasAssistant(user as Assistant)"
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

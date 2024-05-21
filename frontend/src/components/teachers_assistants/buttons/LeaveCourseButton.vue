<script setup lang="ts">
import Button from 'primevue/button';
import { PrimeIcons } from 'primevue/api';
import { type Course } from '@/types/Course.ts';
import { type User } from '@/types/users/User.ts';
import { useMessagesStore } from '@/store/messages.store.ts';
import { useI18n } from 'vue-i18n';
import { useTeacher } from '@/composables/services/teacher.service';
import { useAssistant } from '@/composables/services/assistant.service';
import { ref } from 'vue';

/* Props */
const props = defineProps<{ user: User; course: Course }>();

/* Composable injections */
const { addSuccessMessage, addErrorMessage } = useMessagesStore();
const { teachers, teacherLeaveCourse, getTeachersByCourse } = useTeacher();
const { assistants, assistantLeaveCourse, getAssistantsByCourse } = useAssistant();
const { t } = useI18n();

/* State */
const courseValue = ref<Course>(props.course);

/**
 * Leave the course.
 */
async function leaveCourse(): Promise<void> {
    try {
        // Depending on the user's role, call the correct service
        if (props.user.getRole() === 'types.roles.assistant') {
            await assistantLeaveCourse(courseValue.value.id, props.user.id);
        } else {
            await teacherLeaveCourse(courseValue.value.id, props.user.id);
        }

        addSuccessMessage(
            t('toasts.messages.success'),
            t('toasts.messages.courses.teachersAndAssistants.leave.success', [props.user.getFullName()]),
        );

        // Refresh the course data
        await refreshCourse();
    } catch (error) {
        addErrorMessage(
            t('toasts.messages.error'),
            t('toasts.messages.courses.teachersAndAssistants.leave.error', [props.user.getFullName()]),
        );
    }
}

/* Refreshes the course data by updating the teachers/assistants */
async function refreshCourse(): Promise<void> {
    // Get the new teachers and assistants
    await getTeachersByCourse(courseValue.value.id);
    await getAssistantsByCourse(courseValue.value.id);

    // Set the new course data
    courseValue.value.assistants = assistants.value ?? [];
    courseValue.value.teachers = teachers.value ?? [];
}
</script>

<template>
    <Button
        :icon="PrimeIcons.TRASH"
        icon-pos="right"
        class="p-button-danger p-button-text p-button-rounded"
        @click="leaveCourse"
    />
</template>

<style scoped lang="scss"></style>

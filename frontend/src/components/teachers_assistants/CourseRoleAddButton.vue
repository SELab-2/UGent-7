<script setup lang="ts">
import SelectButton from 'primevue/selectbutton';
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
const { teachers, teacherJoinCourse, teacherLeaveCourse, getTeachersByCourse } = useTeacher();
const { assistants, assistantJoinCourse, assistantLeaveCourse, getAssistantsByCourse } = useAssistant();
const { t } = useI18n();

/* State */
const courseValue = ref<Course>(props.course);
const selectedRole = ref<string>('');

/* Options */
const options = [
    { label: t('views.courses.teachers_and_assistants.search.no_role'), value: '' },
    { label: t('types.roles.assistant'), value: 'assistant' },
    { label: t('types.roles.teacher'), value: 'teacher' },
];

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
    await getTeachersByCourse(props.course.id);
    courseValue.value.teachers = teachers.value ?? [];
}
</script>

<template>
    <div class="p-selectbutton">
        <SelectButton v-model="selectedRole" :options="options" option-value="value" option-label="label" :allow-empty="false" />
    </div>
</template>

<style scoped lang="scss">
.p-selectbutton {
    display: flex;
    justify-content: center; // Aligns items to the right
    height: 90%;
    max-inline-size: 300px;
}

</style>

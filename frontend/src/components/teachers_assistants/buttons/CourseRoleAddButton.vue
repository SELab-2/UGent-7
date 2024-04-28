<script setup lang="ts">
import SelectButton from 'primevue/selectbutton';
import { type Course } from '@/types/Course.ts';
import { type User } from '@/types/users/User.ts';
import { useMessagesStore } from '@/store/messages.store.ts';
import { useI18n } from 'vue-i18n';
import { useTeacher } from '@/composables/services/teacher.service';
import { useAssistant } from '@/composables/services/assistant.service';
import { onMounted, ref, watch } from 'vue';

/* Props */
const props = defineProps<{ user: User; course: Course }>();

/* Composable injections */
const { addSuccessMessage, addErrorMessage } = useMessagesStore();
const { teachers, teacherJoinCourse, teacherLeaveCourse, getTeachersByCourse } = useTeacher();
const { assistants, assistantJoinCourse, assistantLeaveCourse, getAssistantsByCourse } = useAssistant();
const { t } = useI18n();

/* State */
const courseValue = ref<Course>(props.course);
const selectedRole = ref<string | null>(null);

/* Options */
const options = [
    { label: t('views.courses.teachersAndAssistants.search.no_role'), value: '' },
    { label: t('types.roles.assistant'), value: 'assistant' },
    { label: t('types.roles.teacher'), value: 'teacher' },
];

/* Set the role of the user in the course */
onMounted(async () => {
    if (courseValue.value.teachers !== null && courseValue.value.assistants !== null) {
        // Check if the user is a teacher or assistant in the course, if so set the role
        if (courseValue.value.teachers.some((teacher) => teacher.id === props.user.id)) {
            selectedRole.value = 'teacher';
        } else if (courseValue.value.assistants.some((assistant) => assistant.id === props.user.id)) {
            selectedRole.value = 'assistant';
        } else {
            selectedRole.value = '';
        }
    }
});

/**
 * Enroll the user in the course.
 */
async function joinCourse(newValue: string): Promise<void> {
    try {
        // Depending on the new selected value, join the course
        if (newValue === 'assistant') {
            await assistantJoinCourse(courseValue.value.id, props.user.id);
        } else {
            await teacherJoinCourse(courseValue.value.id, props.user.id);
        }

        addSuccessMessage(
            t('toasts.messages.success'),
            t('toasts.messages.courses.teachersAndAssistants.enroll.success', [
                props.user.getFullName(),
                t(`types.roles.${selectedRole.value}`),
            ]),
        );

        // Refresh the course data
        await refreshCourse();
    } catch (error) {
        addErrorMessage(
            t('toasts.messages.error'),
            t('toasts.messages.courses.teachersAndAssistants.enroll.error', [
                props.user.getFullName(),
                t(`types.roles.${selectedRole.value}`),
            ]),
        );
    }
}

/**
 * Leave the course.
 */
async function leaveCourse(oldValue: string, showMessage: boolean = true): Promise<void> {
    try {
        // Depending on the old value, leave the course
        if (oldValue === 'assistant') {
            await assistantLeaveCourse(courseValue.value.id, props.user.id);
        } else {
            await teacherLeaveCourse(courseValue.value.id, props.user.id);
        }

        // Only show the message if parameter is set to true. This is because when changing roles assistant <=> teacher
        // we don't want a leave as .. + join as .. message
        if (showMessage) {
            addSuccessMessage(
                t('toasts.messages.success'),
                t('toasts.messages.courses.teachersAndAssistants.leave.success', [props.user.getFullName()]),
            );
        }

        // Refresh the course data
        await refreshCourse();
    } catch (error) {
        addErrorMessage(
            t('toasts.messages.error'),
            t('toasts.messages.courses.teachersAndAssistants.leave.error', [props.user.getFullName()]),
        );
    }
}

/* Listen for changes to the role selection */
watch(selectedRole, async (newValue, oldValue) => {
    // Make sure the oldValue is not null (this is the initial value)
    if (oldValue !== null) {
        // If the newValue is empty, this means the user is leaving the course
        if (newValue === '') {
            await leaveCourse(oldValue);
        } else {
            // If the oldValue is not empty, this means the user is changing roles. Remove the user from the old role
            if (oldValue !== '') {
                await leaveCourse(oldValue, false);
            }

            // Add the user to the new role
            if (newValue !== null) {
                await joinCourse(newValue);
            }
        }
    }
});

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
    <div class="p-selectbutton">
        <SelectButton
            v-model="selectedRole"
            :options="options"
            option-value="value"
            option-label="label"
            :allow-empty="false"
        />
    </div>
</template>

<style scoped lang="scss">
.p-selectbutton {
    display: flex;
    justify-content: center;
    height: 90%;
    max-inline-size: 300px;
}
</style>

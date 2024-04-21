<script setup lang="ts">
import Card from 'primevue/card';
import CourseRoleAddButton from '@/components/teachers_assistants/CourseRoleAddButton.vue';
import { type User } from '@/types/users/User.ts';
import { type Course } from '@/types/Course';
import { useI18n } from 'vue-i18n';

/* Component props */
const props = defineProps<{ userValue: User; course: Course; detail?: boolean }>();

/* Composable injections */
const { t } = useI18n();
</script>

<template>
    <Card class="course-card">
        <template #title>
            <h2 class="text-primary m-0 text-xl">{{ props.userValue.getFullName() }}</h2>
        </template>
        <template #subtitle v-if="props.detail">
            <span class="text-sm">{{ t(props.userValue.getRole()) }}</span>
        </template>
        <template #content>
            {{ props.userValue.email }}
        </template>
        <!-- Display add/remove button on the assistant/teacher card, only when the user is a-->
        <template #footer v-if="!props.detail">
            <CourseRoleAddButton :user="props.userValue" :course="course" />
        </template>
    </Card>
</template>

<style lang="scss">
.course-card {
    display: flex;
    flex-direction: column;
    height: 100%;
}
</style>

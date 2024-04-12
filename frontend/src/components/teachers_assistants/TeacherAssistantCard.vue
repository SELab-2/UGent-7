<script setup lang="ts">
import Card from 'primevue/card';
import { type User } from '@/types/users/User.ts';
import { type Course } from '@/types/Course';
import { useI18n } from 'vue-i18n';
import TeacherAssistantCourseAddButton from './TeacherAssistantCourseAddButton.vue';

/* Component props */
defineProps<{
    user: User,
    course: Course,
}>();

/* Composable injections */
const { t } = useI18n();
</script>

<template>
    <Card class="border-round course-card">
        <template #title>
            <h2 class="text-primary m-0 text-xl">{{ user.getFullName() }}</h2>
        </template>
        <template #subtitle>
            <span class="text-sm">{{ t(user.getRole()) }}</span>
        </template>
        <template #content>
            {{ user.email }}
        </template>
        <template #footer>
            <TeacherAssistantCourseAddButton :user="user" :course="course" />
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

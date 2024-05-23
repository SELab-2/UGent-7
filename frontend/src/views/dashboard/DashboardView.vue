<script setup lang="ts">
import BaseLayout from '@/views/layout/base/BaseLayout.vue';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';
import StudentDashboardView from '@/views/dashboard/roles/StudentDashboardView.vue';
import TeacherDashboardView from './roles/TeacherDashboardView.vue';
import AssistantDashboardView from './roles/AssistantDashboardView.vue';
import { type Student } from '@/types/users/Student';
import { type Teacher } from '@/types/users/Teacher';
import { type Assistant } from '@/types/users/Assistant';

/* Service injection */
const { user } = storeToRefs(useAuthStore());
</script>

<template>
    <BaseLayout>
        <StudentDashboardView v-if="user?.isStudent()" :student="user as Student" />
        <TeacherDashboardView v-else-if="user?.isTeacher()" :teacher="user as Teacher" />
        <AssistantDashboardView v-else-if="user?.isAssistant()" :assistant="user as Assistant" />
    </BaseLayout>
</template>

<style scoped></style>

<script setup lang="ts">
import BaseLayout from '@/components/layout/BaseLayout.vue';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';
import { type Student } from '@/types/users/Student';
import { type Teacher } from '@/types/users/Teacher';
import { type Assistant } from '@/types/users/Assistant';
import StudentProjectView from '@/views/projects/roles/StudentProjectView.vue';
import TeacherProjectView from '@/views/projects/roles/TeacherProjectView.vue';
import AssistantProjectView from '@/views/projects/roles/AssistantProjectView.vue';

/* Service injection */
const { user } = storeToRefs(useAuthStore());
</script>

<template>
    <BaseLayout>
        <StudentProjectView v-if="user?.isStudent()" :student="user as Student" />
        <TeacherProjectView v-else-if="user?.isTeacher()" :teacher="user as Teacher" />
        <AssistantProjectView v-else-if="user?.isAssistant()" :assistant="user as Assistant" />
    </BaseLayout>
</template>

<style scoped></style>

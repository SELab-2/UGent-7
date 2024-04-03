<script setup lang="ts">
import BaseLayout from '@/components/layout/BaseLayout.vue';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';
import StudentDashboardView from '@/views/dashboard/roles/StudentDashboardView.vue';
import { Student } from '@/types/users/Student';

/* Service injection */
const { user } = storeToRefs(useAuthStore());
</script>

<template>
    <BaseLayout>
        <StudentDashboardView v-if="user?.isStudent()" :student="user as Student" />
    </BaseLayout>
</template>

<style scoped></style>

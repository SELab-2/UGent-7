<script setup lang="ts">
import BaseLayout from '@/components/layout/BaseLayout.vue';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';
import StudentDashboardView from '@/views/dashboard/roles/StudentDashboardView.vue';

/* Service injection */
const { user } = storeToRefs(useAuthStore());
</script>

<template>
    <BaseLayout>
        <StudentDashboardView v-if="user?.isStudent()" :student="user" />
    </BaseLayout>
</template>

<style scoped></style>

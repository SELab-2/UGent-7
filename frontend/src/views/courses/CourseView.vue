<script setup lang="ts">
import BaseLayout from '@/components/layout/base/BaseLayout.vue';
import StudentCourseView from './roles/StudentCourseView.vue';
import TeacherCourseView from './roles/TeacherCourseView.vue';
import AssistantCourseView from './roles/AssistantCourseView.vue';
import { onMounted } from 'vue';
import { useCourses } from '@/composables/services/courses.service.ts';
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';

/* Service injection */
const { user } = storeToRefs(useAuthStore());
const { params } = useRoute();
const { course, getCourseByID } = useCourses();

onMounted(() => {
    getCourseByID(params.courseId as string);
});
</script>

<template>
    <BaseLayout>
        <div v-if="course">
            <StudentCourseView v-if="user?.isStudent()" :course="course" />
            <TeacherCourseView v-else-if="user?.isTeacher()" :course="course" />
            <AssistantCourseView v-else-if="user?.isAssistant()" :course="course" />
        </div>
    </BaseLayout>
</template>

<style scoped lang="scss"></style>

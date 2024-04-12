<script setup lang="ts">
import Title from '@/components/layout/Title.vue';
import ProjectList from '@/components/projects/ProjectList.vue';
import TeacherAssistantList from '@/components/teachers_assistants/TeacherAssistantCourseList.vue';
import { type Course } from '@/types/Course.ts';
import { useI18n } from 'vue-i18n';

/* Props */
const props = defineProps<{
    course: Course;
}>();

/* Composable injections */
const { t } = useI18n();
</script>

<template>
    <!-- Course heading -->
    <div class="flex justify-content-between align-items-center mb-6">
        <!-- Course title -->
        <Title class="m-0">{{ props.course.name }}</Title>
    </div>
    <!-- Description -->
    <p>{{ props.course.description }}</p>
    <!-- Project heading -->
    <div class="flex justify-content-between align-items-center my-6">
        <!-- Project list title -->
        <Title class="m-0">{{ t('views.dashboard.projects') }}</Title>
    </div>
    <!-- Project list body -->
    <ProjectList :courses="[course]" />

    <!-- Heading for teachers and assistants -->
    <div class="flex justify-content-between align-items-center my-6">
        <Title class="m-0">{{ t('views.courses.teachers_and_assistants.title') }}</Title>
    </div>

    <!-- List with teachers and assistants -->
    <TeacherAssistantList :course="props.course" />
</template>

<style scoped lang="scss"></style>

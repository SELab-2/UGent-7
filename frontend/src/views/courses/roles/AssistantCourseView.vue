<script setup lang="ts">
import Title from '@/components/layout/Title.vue';
import ProjectList from '@/components/projects/ProjectList.vue';
import TeacherAssistantList from '@/components/teachers_assistants/TeacherAssistantList.vue';
import { type Course } from '@/types/Course.ts';
import { useI18n } from 'vue-i18n';
import ProjectCreateButton from '@/components/projects/ProjectCreateButton.vue';
import { watch } from 'vue';
import { useProject } from '@/composables/services/project.service.ts';

/* Props */
const props = defineProps<{
    course: Course;
}>();

/* Composable injections */
const { t } = useI18n();
const { projects, getProjectsByCourse } = useProject();

watch(
    () => props.course,
    async () => {
        await getProjectsByCourse(props.course.id);
    },
    { immediate: true },
);
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

        <!-- Create project button -->
        <div v-tooltip.top="t('views.projects.create')">
            <ProjectCreateButton :courses="[props.course]" />
        </div>
    </div>
    <!-- Project list body -->
    <ProjectList :projects="projects" />
    <!-- Heading for teachers and assistants -->
    <div class="flex justify-content-between align-items-center my-6">
        <Title class="m-0">{{ t('views.courses.teachers_and_assistants.title') }}</Title>
    </div>

    <!-- List with teachers and assistants -->
    <TeacherAssistantList :course="props.course" :users="course.teachers.concat(course.assistants)" />
</template>

<style scoped lang="scss"></style>

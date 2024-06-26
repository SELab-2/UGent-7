<script setup lang="ts">
import Title from '@/views/layout/Title.vue';
import ProjectList from '@/components/projects/ProjectList.vue';
import TeacherAssistantList from '@/components/instructors/TeacherAssistantList.vue';
import ProjectCreateButton from '@/components/projects/ProjectCreateButton.vue';
import { type Course } from '@/types/Course.ts';
import { useI18n } from 'vue-i18n';
import { computed } from 'vue';
import { useProject } from '@/composables/services/project.service.ts';
import { watchImmediate } from '@vueuse/core';
import Loading from '@/components/Loading.vue';

/* Props */
const props = defineProps<{
    course: Course;
}>();

/* Composable injections */
const { t } = useI18n();
const { projects, getProjectsByCourse } = useProject();

/* State */
const instructors = computed(() => {
    return props.course.teachers.concat(props.course.assistants);
});

/* Fetch projects when the course changes */
watchImmediate(
    () => props.course.id,
    async (courseId: string) => {
        await getProjectsByCourse(courseId);
    },
);
</script>

<template>
    <!-- Course heading -->
    <div class="flex justify-content-between align-items-center mb-5">
        <!-- Course title -->
        <Title class="m-0">{{ props.course.name }}</Title>
    </div>

    <!-- Description -->
    <div v-html="props.course.description" />

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
    <template v-if="projects !== null">
        <ProjectList :projects="projects">
            <template #empty>
                <p>
                    {{ t('views.courses.noProjects') }}
                </p>

                <ProjectCreateButton :courses="[course]" :label="t('components.button.createProject')" />
            </template>
        </ProjectList>
    </template>
    <template v-else>
        <Loading />
    </template>

    <!-- Heading for teachers and assistants -->
    <div class="flex justify-content-between align-items-center my-6">
        <Title class="m-0">{{ t('views.courses.teachersAndAssistants.title') }}</Title>
    </div>

    <!-- List with teachers and assistants -->
    <TeacherAssistantList :course="props.course" :users="instructors" />
</template>

<style scoped lang="scss"></style>

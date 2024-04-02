<script setup lang="ts">
import { Course } from '@/types/Course.ts';
import { watch } from 'vue';
import { useProject } from '@/composables/services/project.service.ts';
import ProjectCard from '@/components/projects/ProjectCard.vue';
import { useI18n } from 'vue-i18n';

/* Props */
const props = withDefaults(defineProps<{
    courses: Course[];
}>(), {
    courses: []
});

/* Composables */
const { t } = useI18n();
const { projects, getProjectsByCourse } = useProject();

watch(
    () => props.courses,
    async (courses: Course[]) => {
        for (const course of courses) {
            // Fetch the projects for the course
            await getProjectsByCourse(course.id);

            // Assign the course to the projects
            projects.value?.forEach((project) => {
                project.course = course;
            });

            // Assign the projects to the course
            course.projects = projects.value ?? [];
        }
    },
    {
        immediate: true,
    },
);
</script>

<template>
    <template v-if="courses.length > 0">
        <div class="grid align-items-stretch">
            <div
                class="col-12 md:col-6 lg:col-4 xl:col-3"
                v-for="project in courses.flatMap((course) => course.projects)"
                :key="project.id"
            >
                <ProjectCard class="h-100" :project="project" :course="project.course" />
            </div>
        </div>
    </template>
    <template v-else>
        <div class="col-12">
            <p>{{ t('views.dashboard.no_projects') }}</p>
        </div>
    </template>
</template>

<style scoped lang="scss">

</style>
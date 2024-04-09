<script setup lang="ts">
import { type Course } from '@/types/Course.ts';
import { computed, watch } from 'vue';
import { useProject } from '@/composables/services/project.service.ts';
import ProjectCard from '@/components/projects/ProjectCard.vue';
import { useI18n } from 'vue-i18n';
import moment from 'moment';

/* Props */
const props = withDefaults(
    defineProps<{
        courses: Course[];
        showPast?: boolean;
    }>(),
    {
        courses: () => [],
        showPast: false,
    },
);

/* Composables */
const { t } = useI18n();
const { projects, getProjectsByCourse } = useProject();

/* State */

// The merged projects from all courses
const allProjects = computed(() => props.courses.flatMap((course) => course.projects));

/**
 * Sorts the projects by deadline
 */
const sortedProjects = computed(() => {
    const projects = allProjects.value.filter((project) =>
        !props.showPast ? moment(project.deadline).isAfter() : true,
    );

    return [...projects].sort((a, b) => new Date(a.deadline).getTime() - new Date(b.deadline).getTime());
});

/* Watchers */
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
    <template v-if="allProjects.length > 0">
        <div class="grid align-items-stretch">
            <div class="col-12 md:col-6 lg:col-4 xl:col-3" v-for="project in sortedProjects" :key="project.id">
                <ProjectCard class="h-100" :project="project" :course="project.course" v-if="project.course !== null" />
            </div>
        </div>
    </template>
    <template v-else>
        <div class="col-12">
            <p>{{ t('views.dashboard.no_projects') }}</p>
        </div>
    </template>
</template>

<style scoped lang="scss"></style>

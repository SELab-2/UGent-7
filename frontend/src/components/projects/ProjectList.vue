<script setup lang="ts">
import { type Course } from '@/types/Course.ts';
import { computed, ref, watch } from 'vue';
import { useProject } from '@/composables/services/project.service.ts';
import ProjectCard from '@/components/projects/ProjectCard.vue';
import { useI18n } from 'vue-i18n';
import moment from 'moment';
import Skeleton from 'primevue/skeleton';
import InputSwitch from 'primevue/inputswitch';

/* Props */
const props = withDefaults(
    defineProps<{
        courses: Course[] | null;
        cols?: number;
    }>(),
    {
        courses: () => [],
        cols: 4,
    },
);

/* Composables */
const { t } = useI18n();
const { projects, getProjectsByCourse } = useProject();

/* State */
const showPast = ref(false);

// The merged projects from all courses
const allProjects = computed(() => props.courses?.flatMap((course) => course.projects) ?? null);

/**
 * Sorts the projects by deadline
 */
const sortedProjects = computed(() => {
    const projects =
        allProjects.value?.filter((project) => (!showPast.value ? moment(project.deadline).isAfter() : true)) ?? null;

    if (projects === null) {
        return projects;
    }

    return [...projects].sort((a, b) => new Date(a.deadline).getTime() - new Date(b.deadline).getTime());
});

/* Watchers */
watch(
    () => props.courses,
    async (courses: Course[] | null) => {
        if (courses !== null) {
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
        }
    },
    {
        immediate: true,
    },
);
</script>

<template>
    <!-- Show past projects switch -->
    <div class="flex gap-3 align-items-center mb-5">
        <InputSwitch input-id="show-past" v-model="showPast" />
        <label for="show-past">
            {{ t('views.dashboard.showPastProjects') }}
        </label>
    </div>
    <!-- Project list -->
    <div class="grid align-items-stretch">
        <template v-if="sortedProjects !== null">
            <template v-if="sortedProjects.length > 0">
                <div
                    class="col-12 md:col-6 lg:col-4"
                    :class="'xl:col-' + 12 / cols"
                    v-for="project in sortedProjects"
                    :key="project.id"
                >
                    <ProjectCard
                        class="h-100"
                        :project="project"
                        :course="project.course"
                        v-if="project.course !== null"
                    />
                </div>
            </template>
            <template v-else>
                <div class="col-12">
                    <p>{{ t('views.dashboard.no_projects') }}</p>
                </div>
            </template>
        </template>
        <template v-else>
            <div class="col-12 md:col-6 lg:col-4" :class="'xl:col-' + 12 / cols" v-for="index in cols" :key="index">
                <Skeleton height="25rem" />
            </div>
        </template>
    </div>
</template>

<style scoped lang="scss"></style>

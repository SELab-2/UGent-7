<script setup lang="ts">
import moment from 'moment';
import BaseLayout from '@/components/layout/BaseLayout.vue';
import ProjectCard from '@/components/projects/ProjectCard.vue';
import Calendar from 'primevue/calendar';
import Title from '@/components/layout/Title.vue';
import { useProject } from '@/composables/services/project.service';
import { computed, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';
import { type Project } from '@/types/Projects.ts';
import { type RoleUser } from '@/types/users/Generics.ts';

/* Composable injections */
const { t, locale } = useI18n();

/* Component state */
const allProjects = ref<Project[]>([]);
const selectedDate = ref(new Date());

/* Service injection */
const { user } = storeToRefs(useAuthStore());
const { projects, getProjectsByCourse } = useProject();

const formattedDate = computed(() => {
    // Format the selected date using moment.js
    return moment(selectedDate.value)
        .locale(locale.value)
        .format('DD MMMM YYYY');
});

const loadProjects = async (): Promise<void> => {
    if (user.value !== null) {
        // Clear the old data, so that the data from another role is not displayed
        allProjects.value = [];

        // Load the projects of the courses
        if (user.value.isSpecificRole()) {
            // Cast the generic user to a specific role
            const role = user.value as RoleUser;

            for (const course of role.courses) {
                await getProjectsByCourse(course.id);

                // Assign the course to the project
                projects.value?.forEach((project) => {
                    project.course = course;
                });

                // Concatenate the projects
                allProjects.value = allProjects.value.concat(
                    projects.value ?? [],
                );
            }
        }
    }
};

/* Filter the projects on the date selected on the calendar */
const projectsWithDeadline = computed(() => {
    // Filter the projects with the selected date
    return allProjects.value?.filter((project) => {
        return moment(project.deadline).isSame(
            moment(selectedDate.value),
            'day',
        );
    });
});

watch(
    user,
    async () => {
        await loadProjects();
    },
    { immediate: true },
);
</script>

<template>
    <BaseLayout>
        <div class="grid">
            <div class="col-12 md:col-6">
                <!-- Calendar heading -->
                <Title class="mb-6">{{ t('views.calendar.title') }}</Title>

                <div>
                    <!-- Calendar itself -->
                    <Calendar class="w-full" v-model="selectedDate" inline />
                </div>
            </div>
            <div class="col-12 md:col-6">
                <!-- Selected date on the calendar -->
                <Title class="mb-6">{{ formattedDate }}</Title>

                <!-- Listing projects with given deadline -->
                <div class="grid grid-cols-2 gap-4">
                    <div
                        v-for="project in projectsWithDeadline"
                        :key="project.id">
                        <ProjectCard
                            class="h-100"
                            :project="project"
                            :course="project.course" />
                    </div>
                </div>
            </div>
        </div>
    </BaseLayout>
</template>

<style scoped lang="scss"></style>

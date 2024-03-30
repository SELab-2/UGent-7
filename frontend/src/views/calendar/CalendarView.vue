<script setup lang="ts">
import moment from 'moment';
import BaseLayout from '@/components/layout/BaseLayout.vue';
import ProjectLink from '@/components/projects/ProjectLink.vue';
import Calendar from 'primevue/calendar';
import Title from '@/components/layout/Title.vue';
import {useProject} from '@/composables/services/project.service';
import {useCourses} from '@/composables/services/courses.service';
import { computed, onMounted } from 'vue';
import {useI18n} from 'vue-i18n';
import {ref} from 'vue';
import {useAuthStore} from '@/store/authentication.store.ts';
import {Project} from "@/types/Projects.ts";

/* Composable injections */
const { t, locale } = useI18n();

/* Component state */
const allProjects = ref<Project[]>([]);
const selectedDate = ref(new Date());

/* Service injection */
const { user } = useAuthStore();
const { courses, getCoursesByStudent } = useCourses();
const { projects, getProjectsByCourse } = useProject();

const formattedDate = computed(() => {
    // Format the selected date using moment.js
    return moment(selectedDate.value).locale(locale.value).format('DD MMMM YYYY');
});

const loadProjects = async () => {
    if (user !== null) {
        // Load the courses of the student
        await getCoursesByStudent(user.id);

        // Load the projects of the courses
        for (const course of courses.value ?? []) {
            await getProjectsByCourse(course.id);

            // Assign the course to the project
            projects.value?.forEach(project => {
                project.course = course;
            });

            // Concatenate the projects
            allProjects.value = allProjects.value.concat(projects.value ?? []);
        }
    }
};

/* Filter the projects on the date selected on the calendar */
const projectsWithDeadline = computed(() => {
    // Filter the projects with the selected date
    return allProjects.value?.filter(project => {
        return moment(project.deadline).isSame(moment(selectedDate.value), 'day');
    });
});

/* Load the projects when the component is mounted */
onMounted(async () => {
    await loadProjects();
});

</script>

<template>
    <BaseLayout>
        <div class="grid">
            <div class="col-12 md:col-6">
                <!-- Calendar heading -->
                <Title class="mb-6">{{ t('views.calendar.title') }}</Title>

                <div>
                    <!-- Calendar itself -->
                    <Calendar class="w-full" v-model="selectedDate" inline/>
                </div>
            </div>
            <div class="col-12 md:col-6">
                <!-- Selected date on the calendar -->
                <Title class="mb-6">{{ formattedDate }}</Title>

                <!-- Listing projects with given deadline -->
                <div>
                    <div class="col-12" v-for="project in projectsWithDeadline" :key="project.id">
                        <!-- Each ProjectLink card -->
                        <ProjectLink class="h-100 mb-2" :project="project"/>
                    </div>
                </div>
            </div>
        </div>
    </BaseLayout>
</template>

<style scoped lang="scss">

</style>
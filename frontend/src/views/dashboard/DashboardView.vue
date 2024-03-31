<script setup lang="ts">
import Skeleton from 'primevue/skeleton';
import ButtonGroup from 'primevue/buttongroup';
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';
import CourseCard from '@/components/courses/CourseCard.vue';
import BaseLayout from '@/components/layout/BaseLayout.vue';
import Title from '@/components/layout/Title.vue';
import {useI18n} from 'vue-i18n';
import {PrimeIcons} from 'primevue/api';
import { ref, onMounted, watch } from 'vue';
import {Project} from "@/types/Projects.ts";
import {useProject} from "@/composables/services/project.service.ts";
import ProjectCard from "@/components/projects/ProjectCard.vue";
import {useAuthStore} from '@/store/authentication.store.ts';
import {storeToRefs} from 'pinia';
import { computed } from 'vue';
import { Course } from '@/types/Course';

/* Composable injections */
const {t} = useI18n();

/* Component state */
const allProjects = ref<Project[]>([]);
const allCourses = ref<Course[]>([]);
const academicYears = ref<{ label: string; value: number }[]>();
const selectedCoursesYear = ref<number>();
const selectedProjectsYear = ref<number>();

/* Service injection */
const { user } = storeToRefs(useAuthStore());
const { projects, getProjectsByCourse } = useProject();

onMounted(async () => {
    await fetchDashboardData();
    selectedCoursesYear.value = getCurrentAcademicYear();
    selectedProjectsYear.value = getCurrentAcademicYear();
});

watch(user, async () => {
    await fetchDashboardData();
    selectedCoursesYear.value = getCurrentAcademicYear();
    selectedProjectsYear.value = getCurrentAcademicYear();
});

/* Fetch the data for the dashboard */
const fetchDashboardData = async () => {
    if (user.value !== null) {
        // Clear the old data, so that the data from another role is not displayed
        allProjects.value = [];
        academicYears.value = [];

        for (const course of user.value.courses) {
            await getProjectsByCourse(course.id);

            projects.value?.forEach(project => {
                project.course = course;
            });

            allProjects.value = allProjects.value.concat(projects.value ?? []);

            // Add the academic year to the list
            const year = course.academic_startyear;
            if (! academicYears.value?.some(el => el.value === year)) {
                academicYears.value?.push({ label: `${year}-${year + 1}`, value: year });
            }
        }

        // Sort the academic years in descending order
        academicYears.value?.sort((a, b) => b.value - a.value);
    }
}

const filteredProjects = computed(() => {
    return allProjects.value ? allProjects.value.filter(project => project.course?.academic_startyear === selectedProjectsYear.value) : [];
});

const filteredCourses = computed(() => {
    return user.value?.courses ? user.value?.courses.filter(course => course.academic_startyear === selectedCoursesYear.value) : [];
});

// Method to get the current academic year
const getCurrentAcademicYear : () => number = () => {
    const today = new Date();
    const currentYear = today.getFullYear();

    if (today.getMonth() >= 9) {
        return currentYear;
    } else {
        return currentYear - 1;
    }
};

</script>

<template>
    <BaseLayout>
        <!-- Course heading -->
        <div class="flex justify-content-between align-items-center mb-6">
            <!-- Course list title -->
            <Title class="m-0">{{ t('views.dashboard.courses') }}</Title>
            <!-- Course list controls -->
            <ButtonGroup>
                <Dropdown v-model="selectedCoursesYear" :options="academicYears" optionLabel="label" 
                          optionValue="value" class="custom-dropdown"/>

                <RouterLink :to="{ name: 'course-create' }" v-if="user?.isTeacher()">
                    <Button :icon="PrimeIcons.PLUS" icon-pos="right" class="custom-button"/>
                </RouterLink>
            </ButtonGroup>
        </div>
        <!-- Course list body -->
        <div class="grid align-items-stretch">
            <template v-if="filteredCourses !== null">
                <template v-if="filteredCourses.length > 0">
                    <div class="col-12 md:col-6 lg:col-4 xl:col-3" v-for="course in filteredCourses">
                        <CourseCard class="h-100" :course="course"/>
                    </div>
                </template>
                <template v-else>
                    <div class="col-12">
                        <p>{{ t('views.dashboard.no_courses') }}</p>
                    </div>
                </template>
            </template>
            <template v-else>
                <div class="col-12 md:col-6 lg:col-4 xl:col-3" v-for="index in 4" :key="index">
                    <Skeleton height="25rem" style="visibility: hidden;"/>
                </div>
            </template>
        </div>
        <!-- Project heading -->
        <div class="flex justify-content-between align-items-center my-6">
            <!-- Project list title -->
            <Title class="m-0">{{ t('views.dashboard.projects') }}</Title>
            <!-- Project list controls -->
            <ButtonGroup>
                <Dropdown v-model="selectedProjectsYear" :options="academicYears" optionLabel="label" 
                          optionValue="value"class="custom-dropdown"/>

                <!-- TODO: Set to create a project-->
                <RouterLink :to="{ name: 'course-create' }" v-if="! user?.isStudent()">
                    <Button :icon="PrimeIcons.PLUS" icon-pos="right" class="custom-button"/>
                </RouterLink>
            </ButtonGroup>
        </div>
        <!-- Project list body -->
        <div class="grid align-items-stretch">
            <template v-if="filteredProjects.length > 0">
                <div class="col-12 md:col-6 lg:col-4 xl:col-3" v-for="project in filteredProjects">
                    <ProjectCard class="h-100" :project="project"/>
                </div>
            </template>
            <template v-else>
                <div class="col-12">
                    <p>{{ t('views.dashboard.no_projects') }}</p>
                </div>
            </template>
        </div>
    </BaseLayout>
</template>

<style scoped>
    .custom-dropdown, .custom-button {
        border-radius: 0;
        height: 50px;
    }
</style>
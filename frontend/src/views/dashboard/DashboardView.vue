<script setup lang="ts">
import ButtonGroup from 'primevue/buttongroup';
import Button from 'primevue/button';
import CourseList from '@/components/courses/CourseList.vue';
import BaseLayout from '@/components/layout/BaseLayout.vue';
import Title from '@/components/layout/Title.vue';
import YearSelector from '@/components/YearSelector.vue';
import { useI18n } from 'vue-i18n';
import { PrimeIcons } from 'primevue/api';
import { ref, watch, computed } from 'vue';
import { useProject } from '@/composables/services/project.service.ts';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';
import { type RoleUser } from '@/types/users/Generics.ts';
import ProjectList from '@/components/projects/ProjectList.vue';

/* Composable injections */
const { t } = useI18n();

/* Component state */
const academicYears = ref<any[]>([]);
const selectedCoursesYear = ref<number>();
const selectedProjectsYear = ref<number>();

/* Service injection */
const { user } = storeToRefs(useAuthStore());
const { projects, getProjectsByCourse } = useProject();

watch(
    user,
    () => {
        fetchDashboardData().then(() => {
            selectedCoursesYear.value = getCurrentAcademicYear();
            selectedProjectsYear.value = getCurrentAcademicYear();
        });
    },
    {
        immediate: true,
    },
);

/**
 * Fetches the projects and academic years for the dashboard
 */
async function fetchDashboardData(): Promise<void> {
    if (user.value !== null) {
        // Clear the old data, so that the data from another role is not displayed.
        academicYears.value = [];

        // All specific roles (students, assistants and teachers) have courses
        if (user.value.isSpecificRole()) {
            // Cast the generic user to a specific role
            const role = user.value as RoleUser;

            for (const course of role.courses) {
                // Add the academic year to the list
                const year = course.academic_startyear;

                if (!academicYears.value?.some((el) => el.value === year)) {
                    academicYears.value?.push({
                        value: year,
                        label: `${year} - ${year + 1}`
                    });
                }
            }

            // Sort the academic years in descending order
            academicYears.value?.sort((a, b) => b - a);
        }
    }
}

/**
 * Get the current academic year
 *
 * @returns The current academic year
 */
function getCurrentAcademicYear(): number {
    const today = new Date();
    const currentYear = today.getFullYear();

    if (today.getMonth() >= 9) {
        return currentYear;
    }

    return currentYear - 1;
}

// Filter the courses based on the selected year
const filteredCourses = computed(() => {
    if (user.value !== null && user.value.isSpecificRole()) {
        const role = user.value as RoleUser;

        return role.courses.filter((course) => course.academic_startyear === selectedCoursesYear.value);
    }

    return [];
});
</script>

<template>
    <BaseLayout>
        <!-- Course heading -->
        <div class="flex justify-content-between align-items-center mb-6">
            <!-- Course list title -->
            <Title class="m-0">{{ t('views.dashboard.courses') }}</Title>
            <!-- Course list controls -->
            <ButtonGroup>
                <YearSelector :years="academicYears" v-model="selectedCoursesYear" />
                <RouterLink :to="{ name: 'course-create' }" v-if="user?.isTeacher()">
                    <Button :icon="PrimeIcons.PLUS" icon-pos="right" class="custom-button" />
                </RouterLink>
            </ButtonGroup>
        </div>
        <!-- Course list body -->
        <CourseList :courses="filteredCourses" />
        <!-- Project heading -->
        <div class="flex justify-content-between align-items-center my-6">
            <!-- Project list title -->
            <Title class="m-0">{{ t('views.dashboard.projects') }}</Title>
            <!-- Project list controls -->
            <ButtonGroup>
                <YearSelector :years="academicYears" v-model="selectedProjectsYear" />
                <!-- TODO: Set to create a project-->
                <RouterLink :to="{ name: 'course-create' }" v-if="!user?.isStudent()">
                    <Button :icon="PrimeIcons.PLUS" icon-pos="right" class="custom-button" />
                </RouterLink>
            </ButtonGroup>
        </div>
        <!-- Project list body -->
        <ProjectList :courses="filteredCourses" />
    </BaseLayout>
</template>

<style scoped></style>

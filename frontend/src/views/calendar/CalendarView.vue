<script setup lang="ts">
import moment from 'moment';
import BaseLayout from '@/components/layout/BaseLayout.vue';
import Calendar, { type CalendarDateSlotOptions } from 'primevue/calendar';
import Title from '@/components/layout/Title.vue';
import ProjectCreateButton from '@/components/projects/ProjectCreateButton.vue';
import Skeleton from 'primevue/skeleton';
import { useProject } from '@/composables/services/project.service';
import { computed, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';
import { type Project } from '@/types/Projects.ts';
import { type RoleUser } from '@/types/users/Generics.ts';
import { useRoute, useRouter } from 'vue-router';

/* Composable injections */
const { t, locale } = useI18n();
const { query } = useRoute();
const { push } = useRouter();

/* Component state */
const allProjects = ref<Project[]|null>(null);
const selectedDate = ref<Date>(getQueryDate());

/* Service injection */
const { user } = storeToRefs(useAuthStore());
const { projects, getProjectsByCourse } = useProject();

/* Formatted date */
const formattedDate = computed(() => {
    // Format the selected date using moment.js
    return moment(selectedDate.value).locale(locale.value).format('DD MMMM YYYY');
});

/* Filter the projects on the date selected on the calendar */
const projectsWithDeadline = computed(() => {
    return allProjects.value?.filter((project) => {
        return moment(project.deadline).isSame(moment(selectedDate.value), 'day');
    }) ?? null;
});

/* Courses that take place on the selected date in the calendar => no display when the date is in the past */
const coursesWithProjectCreationPossibility = computed(() => {
    if (user.value !== null && moment(selectedDate.value).isAfter(moment())) {
        return (user.value as RoleUser).courses.filter((course) => {
            return course.academic_startyear === selectedAcademicYear();
        });
    } else {
        return [];
    }
});

/**
 * Load the projects of the user.
 */
async function loadProjects(): Promise<void> {
    if (user.value !== null) {
        // Clear the old data, so that the data from another role is not displayed
        allProjects.value = null;

        // Load the projects of the courses
        if (user.value.isSpecificRole()) {
            let _allProjects: Project[] = [];

            // Cast the generic user to a specific role
            const role = user.value as RoleUser;

            for (const course of role.courses) {
                await getProjectsByCourse(course.id);

                // Assign the course to the project
                projects.value?.forEach((project) => {
                    project.course = course;
                });

                // Concatenate the projects
                _allProjects = _allProjects.concat(projects.value ?? []);
            }

            allProjects.value = _allProjects;
        }
    }
}

/**
 * Get the date from the query parameters.
 *
 * @returns The date from the query parameters.
 */
function getQueryDate(): Date {
    const queryDate = query.date as string;

    if (queryDate != null) {
        const date = moment(queryDate);

        if (date.isValid()) {
            return date.toDate();
        }
    }

    return moment().toDate();
}

/**
 * Check if the project has a deadline on the given date.
 *
 * @param date
 */
function hasDeadline(date: CalendarDateSlotOptions): boolean {
    const dateObj = new Date(date.year, date.month, date.day);

    return (
        allProjects.value?.some((project) => {
            return moment(project.deadline).isSame(moment(dateObj), 'day');
        }) ?? false
    );
}

/**
 * Count the deadlines on the given date.
 *
 * @param date
 */
function countDeadlines(date: CalendarDateSlotOptions): number {
    const dateObj = new Date(date.year, date.month, date.day);

    return (
        allProjects.value?.filter((project) => {
            return moment(project.deadline).isSame(moment(dateObj), 'day');
        }).length ?? 0
    );
}

/**
 * Get the academic year of the selected date.
 *
 * @returns The academic year of the selected date.
 */
const selectedAcademicYear = (): number => {
    const selectedYear = moment(selectedDate.value).year();
    const selectedMonth = moment(selectedDate.value).month();

    return selectedMonth < 8 ? selectedYear - 1 : selectedYear;
};

/* Watch the user and load the projects */
watch(
    user,
    async () => {
        await loadProjects();
    },
    { immediate: true },
);

watch(selectedDate, (date) => {
    push({ query: { date: moment(date).format('YYYY-MM-DD') } });
});
</script>

<template>
    <BaseLayout>
        <!-- Calendar heading -->
        <Title class="mb-6">{{ t('views.calendar.title') }}</Title>
        <!-- Calendar body -->
        <div class="grid">
            <div class="col-12 md:col-6">
                <div>
                    <!-- Calendar itself -->
                    <Calendar class="w-full" v-model="selectedDate" inline>
                        <template #date="{ date }">
                            <div class="relative">
                                <div class="deadline-indicator" v-if="hasDeadline(date)">
                                    {{ countDeadlines(date) }}
                                </div>
                                <span>{{ date.day }}</span>
                            </div>
                        </template>
                    </Calendar>
                </div>
            </div>
            <div class="col-12 md:col-6">
                <div class="surface-100 p-6">
                    <!-- Selected date on the calendar -->
                    <Title class="mb-6 font-extrabold">
                        {{ formattedDate }}
                    </Title>

                    <!-- Listing projects with given deadline -->
                    <div class="flex flex-column gap-4">
                        <template v-if="projectsWithDeadline !== null">
                            <template v-if="projectsWithDeadline.length > 0">
                                <!-- Project cards -->
                                <div class="flex flex-column xl:flex-row border-round-md" v-for="project in projectsWithDeadline" :key="project.id">
                                    <!-- Icon -->
                                    <div
                                        class="bg-primary flex justify-content-center align-items-center p-4 xl:w-7rem xl:h-7rem"
                                    >
                                        <span class="pi pi-book text-6xl" />
                                    </div>
                                    <!-- Details -->
                                    <div
                                        class="flex flex-column gap-3 justify-content-center bg-white text-black-alpha-80 p-3 w-full"
                                    >
                                        <RouterLink
                                            :to="{
                                            name: 'course-project',
                                            params: {
                                                courseId: project.course?.id,
                                                projectId: project.id,
                                            },
                                        }"
                                        >
                                            <h3 class="flex gap-3 align-items-center text-primary m-0 text-xl">
                                                {{ project.name }} <span class="pi pi-arrow-right text-xl" />
                                            </h3>
                                        </RouterLink>
                                        <p class="font-bold m-0">
                                            {{ project.course?.name }}
                                        </p>
                                    </div>
                                </div>
                            </template>
                            <template v-else>
                                <p class="m-0">{{ t('views.calendar.noProjects') }}</p>
                            </template>
                        </template>
                        <template v-else>
                            <Skeleton height="7rem"/>
                        </template>
                    </div>

                    <template v-if="coursesWithProjectCreationPossibility.length > 0 && user?.isTeacher() || user?.isAssistant()">
                        <!-- Add project button -->
                        <ProjectCreateButton class="mt-5" :label="t('components.button.createProject')" severity="secondary" :courses="coursesWithProjectCreationPossibility" />
                    </template>
                </div>
            </div>
        </div>
    </BaseLayout>
</template>

<style lang="scss">
.p-calendar {
    td > span {
        overflow: visible;
    }
}

.deadline-indicator {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    height: 0.95rem;
    width: 0.95rem;
    color: white;
    position: absolute;
    top: -0.5rem;
    right: -1rem;
    z-index: 2;
    background: indianred;
    border-radius: 50%;
}
</style>

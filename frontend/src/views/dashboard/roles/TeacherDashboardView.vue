<script setup lang="ts">
import ButtonGroup from 'primevue/buttongroup';
import Button from 'primevue/button';
import Title from '@/views/layout/Title.vue';
import YearSelector from '@/components/YearSelector.vue';
import CourseList from '@/components/courses/CourseDetailList.vue';
import ProjectList from '@/components/projects/ProjectList.vue';
import ProjectCreateButton from '@/components/projects/ProjectCreateButton.vue';
import Loading from '@/components/Loading.vue';
import { type Teacher } from '@/types/users/Teacher';
import { PrimeIcons } from 'primevue/api';
import { useI18n } from 'vue-i18n';
import { computed, ref } from 'vue';
import { useCourses } from '@/composables/services/course.service.ts';
import { getAcademicYear, getAcademicYears } from '@/types/Course.ts';
import { useProject } from '@/composables/services/project.service.ts';
import { watchImmediate } from '@vueuse/core';

/* Props */
const props = defineProps<{
    teacher: Teacher;
}>();

/* Composable injections */
const { t } = useI18n();
const { projects, getProjectsByTeacher } = useProject();
const { courses, getCoursesByTeacher } = useCourses();

/* State */
const loading = ref(true);

const selectedYear = ref(getAcademicYear());
const allYears = computed(() => getAcademicYears(...(courses.value?.map((course) => course.academic_startyear) ?? [])));

const filteredCourses = computed(
    () => courses.value?.filter((course) => course.academic_startyear === selectedYear.value) ?? null,
);

/* Watchers */
watchImmediate(
    () => props.teacher,
    async (teacher: Teacher) => {
        loading.value = true;
        await getCoursesByTeacher(teacher.id);
        await getProjectsByTeacher(teacher.id);
        loading.value = false;
    },
);
</script>

<template>
    <template v-if="!loading">
        <div class="fadein">
            <!-- Project heading -->
            <div
                class="flex gap-5 flex-column md:flex-row justify-content-between align-items-start md:align-items-center mb-5"
            >
                <!-- Project list title -->
                <Title class="m-0">{{ t('views.dashboard.projects') }}</Title>

                <!-- Create project button -->
                <ProjectCreateButton
                    id="projectCreate"
                    v-if="filteredCourses !== null"
                    :courses="filteredCourses"
                    :label="t('components.button.createProject')"
                />
            </div>

            <!-- Project list body -->
            <template v-if="projects !== null && filteredCourses !== null">
                <ProjectList :projects="projects">
                    <template #empty>
                        <template v-if="filteredCourses.length === 0">
                            <p>{{ t('components.list.noCourses.teacher') }}</p>
                            <RouterLink :to="{ name: 'course-create' }">
                                <Button :label="t('components.button.createCourse')" icon="pi pi-plus" />
                            </RouterLink>
                        </template>
                        <template v-else>
                            <p>
                                {{ t('components.list.noProjects.teacher') }}
                            </p>

                            <p v-if="filteredCourses.length === 0">
                                {{ t('components.list.noCourses.teacher') }}
                            </p>

                            <ProjectCreateButton
                                id="projectCreate"
                                :courses="filteredCourses"
                                :label="t('components.button.createProject')"
                            />
                        </template>
                    </template>
                </ProjectList>
            </template>
            <template v-else>
                <Loading />
            </template>

            <!-- Course heading -->
            <div
                class="flex gap-5 flex-column md:flex-row justify-content-between align-items-start md:align-items-center my-6"
            >
                <!-- Course list title -->
                <Title class="m-0">{{ t('views.dashboard.courses') }}</Title>
                <!-- Course list controls -->
                <ButtonGroup class="flex align-items-center">
                    <!-- Academic year selector -->
                    <YearSelector :years="allYears" v-model="selectedYear" />

                    <!-- Create course button -->
                    <RouterLink id="courseCreate" :to="{ name: 'course-create' }">
                        <Button
                            :icon="PrimeIcons.PLUS"
                            icon-pos="right"
                            class="custom-button"
                            style="height: 51px; width: 51px"
                        />
                    </RouterLink>
                </ButtonGroup>
            </div>

            <!-- Course list body -->
            <template v-if="filteredCourses !== null">
                <CourseList :courses="filteredCourses">
                    <template #empty>
                        <p>{{ t('components.list.noCourses.teacher') }}</p>
                        <RouterLink id="courseCreate" :to="{ name: 'course-create' }">
                            <Button :label="t('components.button.createCourse')" icon="pi pi-plus" />
                        </RouterLink>
                    </template>
                </CourseList>
            </template>
            <template v-else>
                <Loading />
            </template>
        </div>
    </template>
    <template v-else>
        <Loading height="70vh" />
    </template>
</template>

<style scoped lang="scss"></style>

<script setup lang="ts">
import Title from '@/views/layout/Title.vue';
import YearSelector from '@/components/YearSelector.vue';
import CourseList from '@/components/courses/CourseDetailList.vue';
import ProjectList from '@/components/projects/ProjectList.vue';
import Loading from '@/components/Loading.vue';
import { type Student } from '@/types/users/Student.ts';
import { useI18n } from 'vue-i18n';
import { computed, ref } from 'vue';
import { useCourses } from '@/composables/services/course.service.ts';
import { getAcademicYear, getAcademicYears } from '@/types/Course.ts';
import { useProject } from '@/composables/services/project.service.ts';
import { watchImmediate } from '@vueuse/core';

/* Props */
const props = defineProps<{
    student: Student;
}>();

/* Composable injections */
const { t } = useI18n();
const { projects, getProjectsByStudent } = useProject();
const { courses, getCoursesByStudent } = useCourses();

/* State */
const loading = ref(true);

const selectedYear = ref(getAcademicYear());
const allYears = computed(() => getAcademicYears(...(courses.value?.map((course) => course.academic_startyear) ?? [])));

const filteredCourses = computed(
    () => courses.value?.filter((course) => course.academic_startyear === selectedYear.value) ?? null,
);

const visibleProjects = computed(() => projects.value?.filter((project) => project.visible) ?? null);

/* Watchers */
watchImmediate(
    () => props.student,
    async (student: Student) => {
        loading.value = true;
        await getCoursesByStudent(student.id);
        await getProjectsByStudent(student.id);
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
            </div>

            <!-- Project list body -->
            <template v-if="visibleProjects !== null">
                <ProjectList class="fadein" :projects="visibleProjects" />
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

                <!-- Academic year selector -->
                <YearSelector :years="allYears" v-model="selectedYear" />
            </div>

            <!-- Course list body -->
            <template v-if="filteredCourses !== null">
                <CourseList class="fadein" :courses="filteredCourses" />
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

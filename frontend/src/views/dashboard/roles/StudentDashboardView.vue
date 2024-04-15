<script setup lang="ts">
import Title from '@/components/layout/Title.vue';
import YearSelector from '@/components/YearSelector.vue';
import CourseList from '@/components/courses/CourseList.vue';
import ProjectList from '@/components/projects/ProjectList.vue';
import { type Student } from '@/types/users/Student.ts';
import { useI18n } from 'vue-i18n';
import { computed, ref, watch } from 'vue';
import { useCourses } from '@/composables/services/course.service.ts';
import { getAcademicYear, getAcademicYears } from '@/types/Course.ts';

/* Props */
const props = defineProps<{
    student: Student;
}>();

/* Composable injections */
const { t } = useI18n();
const { courses, getCoursesByStudent } = useCourses();

/* State */
const selectedYear = ref(getAcademicYear());
const allYears = computed(() => getAcademicYears(...(courses.value?.map((course) => course.academic_startyear) ?? [])));

const filteredCourses = computed(
    () => courses.value?.filter((course) => course.academic_startyear === selectedYear.value) ?? null,
);

/* Watchers */
watch(
    props.student,
    () => {
        getCoursesByStudent(props.student.id);
    },
    {
        immediate: true,
    },
);
</script>

<template>
    <!-- Course heading -->
    <div
        class="flex gap-6 flex-column md:flex-row justify-content-between align-items-start md:align-items-center mb-6"
    >
        <!-- Course list title -->
        <Title class="m-0">{{ t('views.dashboard.courses') }}</Title>

        <!-- Academic year selector -->
        <YearSelector :years="allYears" v-model="selectedYear" />
    </div>
    <!-- Course list body -->
    <CourseList :courses="filteredCourses" />
    <!-- Project heading -->
    <div class="flex justify-content-between align-items-center my-6">
        <!-- Project list title -->
        <Title class="m-0">{{ t('views.dashboard.projects') }}</Title>
    </div>

    <!-- Project list body -->
    <ProjectList :courses="filteredCourses" />
</template>

<style scoped lang="scss"></style>

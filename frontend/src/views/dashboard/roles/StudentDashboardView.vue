<script setup lang="ts">
import Title from '@/components/layout/Title.vue';
import YearSelector from '@/components/YearSelector.vue';
import CourseList from '@/components/courses/CourseList.vue';
import ProjectList from '@/components/projects/ProjectList.vue';
import { type Student } from '@/types/users/Student.ts';
import { useI18n } from 'vue-i18n';
import { computed, ref, watch } from 'vue';
import { useCourses } from '@/composables/services/courses.service.ts';
import { User } from '@/types/users/User.ts';

/* Props */
const props = defineProps<{
    student: Student;
}>();

/* Composable injections */
const { t } = useI18n();
const { courses, getCoursesByStudent } = useCourses();

/* State */
const selectedYear = ref<number>(User.getAcademicYear());

const filteredCourses = computed(
    () => courses.value?.filter((course) => course.academic_startyear === selectedYear.value) ?? [],
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
    <div class="flex justify-content-between align-items-center mb-6">
        <!-- Course list title -->
        <Title class="m-0">{{ t('views.dashboard.courses') }}</Title>

        <!-- Academic year selector -->
        <YearSelector :years="student.academic_years" v-model="selectedYear" />
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

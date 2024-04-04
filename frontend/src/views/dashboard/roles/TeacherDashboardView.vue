<script setup lang="ts">
import ButtonGroup from 'primevue/buttongroup';
import Button from 'primevue/button';
import Title from '@/components/layout/Title.vue';
import YearSelector from '@/components/YearSelector.vue';
import CourseList from '@/components/courses/CourseList.vue';
import ProjectList from '@/components/projects/ProjectList.vue';
import ProjectCreateButton from '@/components/projects/ProjectCreateButton.vue';
import { type Teacher } from '@/types/users/Teacher';
import { PrimeIcons } from 'primevue/api';
import { useI18n } from 'vue-i18n';
import { computed, ref, watch } from 'vue';
import { useCourses } from '@/composables/services/courses.service.ts';
import { User } from '@/types/users/User.ts';

/* Props */
const props = defineProps<{
    teacher: Teacher;
}>();

/* Composable injections */
const { t } = useI18n();
const { courses, getCoursesByTeacher } = useCourses();

/* State */
const selectedYear = ref<number>(User.getAcademicYear());

const filteredCourses = computed(
    () => courses.value?.filter((course) => course.academic_startyear === selectedYear.value) ?? [],
);

/* Watchers */
watch(
    props.teacher,
    () => {
        getCoursesByTeacher(props.teacher.id);
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
        <!-- Course list controls -->
        <ButtonGroup class="flex align-items-center">
            <!-- Academic year selector -->
            <YearSelector :years="teacher.academic_years" v-model="selectedYear" />

            <!-- Create course button -->
            <RouterLink :to="{ name: 'course-create' }">
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
    <CourseList :courses="filteredCourses" />
    <!-- Project heading -->
    <div class="flex justify-content-between align-items-center my-6">
        <!-- Project list title -->
        <Title class="m-0">{{ t('views.dashboard.projects') }}</Title>

        <!-- Create project button -->
        <ProjectCreateButton :courses="filteredCourses" />
    </div>
    <!-- Project list body -->
    <ProjectList :courses="filteredCourses" />
</template>

<style scoped lang="scss"></style>

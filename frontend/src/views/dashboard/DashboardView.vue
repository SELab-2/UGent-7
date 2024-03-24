<script setup lang="ts">
import ButtonGroup from 'primevue/buttongroup';
import Button from 'primevue/button';
import CourseCard from '@/components/courses/CourseCard.vue';
import ProjectCard from '@/components/projects/ProjectCard.vue';
import BaseLayout from '@/components/layout/BaseLayout.vue';
import Title from '@/components/Title.vue';
import {useI18n} from 'vue-i18n';
import {PrimeIcons} from 'primevue/api';
import {onMounted } from 'vue';
import { useCourses } from '@/composables/services/courses.service.ts';
import { useProject } from '@/composables/services/project.service.ts';

/* Composable injections */
const { t } = useI18n();

/* Service injection */
const { courses, getCoursesByStudent } = useCourses();
const { projects, getProjectsByStudent } = useProject();

onMounted(async () => {
  console.log("fetching courses");
  await getCoursesByStudent(1);  // TODO make this the id of the logged in user
  await getProjectsByStudent('1');
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
                <Button :label="t('components.buttons.academic_year', ['2023-2024'])" :icon="PrimeIcons.CHEVRON_DOWN" icon-pos="right" outlined/>
                <Button :icon="PrimeIcons.PLUS" icon-pos="right"/>
            </ButtonGroup>
        </div>
        <!-- Course list body -->
        <div class="grid align-items-stretch">
            <div class="col-12 md:col-6 lg:col-4 xl:col-3" v-for="course in courses">
                <CourseCard class="h-100" :course="course"/>
            </div>
        </div>
        <!-- Project heading -->
        <div class="flex justify-content-between align-items-center my-6">
            <!-- Project list title -->
            <Title class="m-0">{{ t('views.dashboard.projects') }}</Title>
            <!-- Project list controls -->
            <ButtonGroup>
                <Button :label="t('components.buttons.academic_year', ['2023-2024'])" :icon="PrimeIcons.CHEVRON_DOWN" icon-pos="right" outlined/>
                <Button :icon="PrimeIcons.PLUS" icon-pos="right"/>
            </ButtonGroup>
        </div>
        <!-- Project list body -->
        <div class="grid align-items-stretch">
           <div class="col-12 md:col-6 lg:col-4 xl:col-3" v-for="project in projects">
                <ProjectCard class="h-100" :project="project"/>
            </div>

        </div>
    </BaseLayout>
</template>

<style scoped>

</style>
<script setup lang="ts">
import ButtonGroup from 'primevue/buttongroup';
import Button from 'primevue/button';
import CourseCard from '@/components/courses/CourseCard.vue';
import BaseLayout from '@/components/layout/BaseLayout.vue';
import Title from '@/components/layout/Title.vue';
import { useI18n } from 'vue-i18n';
import { PrimeIcons } from 'primevue/api';
import { onMounted } from 'vue';
import { useCourses } from '@/composables/services/courses.service.ts';
import { useStudents } from '@/composables/services/students.service.ts';
import {ref} from 'vue';
import {Project} from "@/types/Projects.ts";
import {useProject} from "@/composables/services/project.service.ts";
import ProjectCard from "@/components/projects/ProjectCard.vue";

/* Composable injections */
const { t } = useI18n();

const allProjects= ref<Project[]>([]);

/* Service injection */
const { projects, getProjectsByCourse } = useProject();
const { courses, getCoursesByStudent, createCourse, deleteCourse } = useCourses();
const { studentJoinCourse } = useStudents();


onMounted(async () => {
  console.log("fetching courses");
  await getCoursesByStudent("1", t);  // TODO make this the id of the logged in user
  // loop through courses and fetch all projects
  let tempProjects: Project[] = [];
  for (const course of courses.value ?? []) {
    await getProjectsByCourse(course.id, t);
    const projectsWithCourse = projects.value?.map(project => ({
      ...project,
      course: course // Voeg de huidige cursus toe aan elk project
    }));
    // Add current course to the received projects
    tempProjects = tempProjects.concat(projectsWithCourse ?? []);
  }
  allProjects.value = tempProjects;
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
            <template v-if="courses !== null">
                <template v-if="courses.length > 0">
                    <div class="col-12 md:col-6 lg:col-4 xl:col-3 fadein" v-for="course in courses">
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
                <Button :label="t('components.buttons.academic_year', ['2023-2024'])" :icon="PrimeIcons.CHEVRON_DOWN" icon-pos="right" outlined/>
                <Button :icon="PrimeIcons.PLUS" icon-pos="right"/>
            </ButtonGroup>
        </div>
        <!-- Project list body -->
        <div class="grid align-items-stretch">
           <div class="col-12 md:col-6 lg:col-4 xl:col-3" v-for="project in allProjects">
                <ProjectCard class="h-100" :project="project"/>
            </div>
        </div>
    </BaseLayout>
</template>

<style scoped>

</style>
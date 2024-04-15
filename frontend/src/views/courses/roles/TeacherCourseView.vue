<script setup lang="ts">
import Title from '@/components/layout/Title.vue';
import ProjectList from '@/components/projects/ProjectList.vue';
import Button from 'primevue/button';
import { type Course } from '@/types/Course.ts';
import { useI18n } from 'vue-i18n';
import { RouterLink } from 'vue-router';
import { PrimeIcons } from 'primevue/api';

/* Props */
const props = defineProps<{
    course: Course;
}>();

/* Composable injections */
const { t } = useI18n();
</script>

<template>
    <!-- Course heading -->
    <div class="flex justify-content-between align-items-center mb-6">
        <!-- Course title -->
        <Title class="m-0">{{ props.course.name }}</Title>

        <!-- Update course button -->
        <RouterLink :to="{ name: 'course-edit', params: { courseId: props.course.id } }">
            <Button
                :icon="PrimeIcons.PENCIL"
                icon-pos="right"
                class="custom-button"
                style="height: 51px; width: 51px"
                aria-label="Update Course"
            />
        </RouterLink>
    </div>
    <!-- Description -->
    <div v-html="props.course.description" />
    <!-- Project heading -->
    <div class="flex justify-content-between align-items-center my-6">
        <!-- Project list title -->
        <Title class="m-0">{{ t('views.dashboard.projects') }}</Title>
    </div>
    <!-- Project list body -->
    <ProjectList :courses="[course]" />
</template>

<style scoped lang="scss"></style>

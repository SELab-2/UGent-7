<script setup lang="ts">
import Title from '@/components/layout/Title.vue';
import Skeleton from 'primevue/skeleton';
import Button from 'primevue/button';
import { type Teacher } from '@/types/users/Teacher.ts';
import { type Project } from '@/types/Project.ts';
import ProjectInfo from '@/components/projects/ProjectInfo.vue';
import DownloadCSVButton from '@/components/projects/DownloadCSVButton.vue';
import ProjectMeter from '@/components/submissions/ProjectMeter.vue';
import { PrimeIcons } from 'primevue/api';

/* Props */
defineProps<{
    teacher: Teacher;
    project: Project | null;
}>();
</script>

<template>
    <template v-if="project !== null">
        <div class="flex align-items-center justify-content-between gap-3">
            <Title class="mb-5">
                {{ project.name }}
            </Title>
            <RouterLink :to="{ name: 'project-edit', params: { courseId: project.course.id, projectId: project.id } }">
                <Button label="Bewerk project" :icon="PrimeIcons.PENCIL"> </Button>
            </RouterLink>
        </div>
    </template>
    <template v-else>
        <Skeleton class="mb-4" height="3rem" width="30rem" />
    </template>
    <div class="grid">
        <div class="col-12 md:col-8">
            <template v-if="project !== null">
                <ProjectInfo class="mb-3" :project="project" />
                <div v-if="project" v-html="project.description" />
            </template>
            <template v-else>
                <Skeleton height="4rem" />
                <Skeleton height="10rem" />
            </template>
        </div>
        <div class="col-12 md:col-4">
            <ProjectMeter :project="project" />
        </div>
        <div class="col-12 md:col-4">
            <template v-if="project !== null">
                <DownloadCSVButton :project="project" />
            </template>
        </div>
    </div>
</template>

<style scoped lang="scss"></style>

<script setup lang="ts">
import Card from 'primevue/card';
import {Project} from '@/types/Projects.ts';

/* Component props */
defineProps<{
    project: Project
}>();


</script>

<template>
  <RouterLink :to="{ name: 'project',  params: { courseId: project.course.id, projectId: project.id } }">
    <Card class="border-round">
      <template #title>
        <h2 class="text-primary m-0 text-2xl">{{ project.name }}</h2>
      </template>
      <template #subtitle>
        <span class="text-sm">{{ project.course.name }}</span>
      </template>
      <template #content>
        <div>{{ project.description }}</div>
      </template>
    </Card>
 </RouterLink>
</template>

<style lang="scss">
</style>
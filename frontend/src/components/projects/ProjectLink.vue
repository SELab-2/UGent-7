<script setup lang="ts">
import Card from 'primevue/card';
import Button from 'primevue/button';
import {Project} from '@/types/Projects.ts';
import {PrimeIcons} from 'primevue/api';

/* Component props */
defineProps<{
    project: Project
}>();


</script>

<template>
    <Card class="border-round">
        <template #title>
            <h2 class="text-primary m-0 text-2xl">{{ project.name }}</h2>
        </template>
        <template #subtitle>
            <span class="text-sm">{{ project.course.name }}</span>
        </template>
        <template #content>
            {{ project.description }}
        </template>
        <template #footer>
            <!-- <RouterLink :to="{ name: 'project-view', params: { id: project.id } }"> -->
            <RouterLink :to="{ name: 'dashboard' }">
                <Button :icon="PrimeIcons.ARROW_RIGHT" icon-pos="right" outlined/>
            </RouterLink>
        </template>
    </Card>
</template>

<style lang="scss">
</style>
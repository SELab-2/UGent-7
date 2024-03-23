<script setup lang="ts">
import Card from 'primevue/card';
import Button from 'primevue/button';
import {Project} from '@/types/Projects.ts';
import {PrimeIcons} from 'primevue/api';
import {useI18n} from 'vue-i18n';

/* Component props */
defineProps<{
  project: Project
}>();

/* Composable injections */
const { t } = useI18n();

/* Default image thumbnails */
const images = Object.keys(import.meta.glob('@/assets/img/placeholders/*', {
  eager: true
}));
</script>

<template>
  <Card class="border-round">
    <template #header>
      <img class="w-full h-12rem border-round-top" style="object-fit: cover; margin-bottom: -4px;" :alt="project.description" :src="images[project.name.length % images.length]"/>
    </template>
    <template #title>
      <h2 class="text-primary m-0 text-2xl">{{ project.name }}</h2>
    </template>
    <template #subtitle>
      <span class="text-sm">{{ project.deadline }}</span>
    </template>
    <template #content>
      {{ project.description }}
    </template>
    <template #footer>
      <RouterLink :to="{ name: 'project-view', params: { id: project.id } }">
        <Button :icon="PrimeIcons.ARROW_RIGHT" :label="t('components.card.open')" icon-pos="right" outlined/>
      </RouterLink>
    </template>
  </Card>
</template>

<style lang="scss">
</style>
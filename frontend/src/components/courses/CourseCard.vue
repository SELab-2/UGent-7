<script setup lang="ts">
import Card from 'primevue/card';
import Button from 'primevue/button';
import {Course} from '@/types/Course.ts';
import {PrimeIcons} from 'primevue/api';
import {useI18n} from 'vue-i18n';

/* Component props */
defineProps<{
    course: Course
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
            <img class="w-full h-12rem border-round-top" style="object-fit: cover; margin-bottom: -4px;" :alt="course.description" :src="images[course.name.length % images.length]"/>
        </template>
        <template #title>
            <h2 class="text-primary m-0 text-2xl">{{ course.name }}</h2>
        </template>
        <template #subtitle>
            <span class="text-sm">{{ course.getCourseYear() }}</span>
        </template>
        <template #content>
            {{ course.description }}
        </template>
        <template #footer>
            <Button :icon="PrimeIcons.ARROW_RIGHT" :label="t('components.card.open')" icon-pos="right" outlined/>
        </template>
    </Card>
</template>

<style lang="scss">
</style>
<script setup lang="ts">
import ButtonGroup from 'primevue/buttongroup';
import Button from 'primevue/button';
import CourseCard from '@/components/courses/CourseCard.vue';
import BaseLayout from '@/components/layout/BaseLayout.vue';
import Title from '@/components/Title.vue';
import {useI18n} from 'vue-i18n';
import {PrimeIcons} from 'primevue/api';
import {ref} from 'vue';
import {Course} from '@/types/Course.ts';

/* Composable injections */
const { t } = useI18n();

/* View data */
const courses = ref([
    new Course(1, 'Information Security Yippee', 'Eric ❤️', 2023),
    new Course(1, 'Computationele Biologie', 'Bachelor opvulvak 🐜', 2023),
    new Course(1, 'Inleiding tot de elektrotechniek', 'Lightning ⚡', 2023),
    new Course(1, 'Mobile and Broadband Access Networks', 'WiFi moment 🛜', 2023),
]);
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

        </div>
    </BaseLayout>
</template>

<style scoped>

</style>
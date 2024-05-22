<script setup lang="ts">
import Card from 'primevue/card';
import Button from 'primevue/button';
import { type Course } from '@/types/Course.ts';
import { PrimeIcons } from 'primevue/api';
import { useI18n } from 'vue-i18n';
import { useGlob } from '@/composables/glob.ts';

/* Component props */
defineProps<{
    course: Course;
}>();

/* Composable injections */
const { t } = useI18n();
const { getRandomImport } = useGlob(import.meta.glob('@/assets/img/placeholders/*.png', { eager: true }));
const { getImport } = useGlob(import.meta.glob('@/assets/img/faculties/*.png', { eager: true }));
</script>

<template>
    <RouterLink :to="{ name: 'course', params: { courseId: course.id } }">
        <Card id="course" class="border-round course-card max-w-30rem">
            <template #header>
                <div class="flex align-items-center justify-content-center text-white relative p-3 text-center h-12rem">
                    <img
                        class="w-full h-12rem border-round-top absolute z-0"
                        style="object-fit: cover"
                        :alt="course.name ?? ''"
                        :src="getRandomImport()"
                    />
                    <div class="bg-black-alpha-40 w-full h-full absolute z-1 border-round-top" />
                    <h2 class="text-white m-0 text-2xl z-2">{{ course.name }}</h2>
                </div>
            </template>
            <template #subtitle>
                <span class="flex gap-2 align-items-center">
                    <img
                        :src="getImport(course.faculty.id + '.png')"
                        :alt="course.faculty.name"
                        class="w-2rem border-circle"
                        v-if="course.faculty !== null"
                    />
                    Academiejaar {{ course.getCourseYear() }}
                </span>
            </template>
            <template #content>
                <div class="flex gap-3 align-items-start">
                    <span>
                        {{ course.getExcerpt() }}
                    </span>
                </div>
            </template>
            <template #footer>
                <slot :course="course" name="footer">
                    <Button
                        :icon="PrimeIcons.ARROW_RIGHT"
                        :label="t('components.card.open')"
                        icon-pos="right"
                        outlined
                    />
                </slot>
            </template>
        </Card>
    </RouterLink>
</template>

<style lang="scss">
.course-card {
    display: flex;
    flex-direction: column;
    height: 100%;
}
</style>

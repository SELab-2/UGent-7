<script setup lang="ts">
import CourseDetailCard from '@/components/courses/CourseDetailCard.vue';
import { type Course } from '@/types/Course.ts';
import { useI18n } from 'vue-i18n';
import { PrimeIcons } from 'primevue/api';
import Button from 'primevue/button';

/* Props */
interface Props {
    cols?: number;
    courses: Course[];
}

withDefaults(defineProps<Props>(), {
    cols: 4,
});

/* Composable injections */
const { t } = useI18n();
</script>

<template>
    <div class="grid align-items-stretch">
        <template v-if="courses.length > 0">
            <div class="col-12 md:col-6" :class="'xl:col-' + 12 / cols" v-for="course in courses" :key="course.id">
                <CourseDetailCard :course="course">
                    <template #footer="{ course }">
                        <slot name="footer" :course="course">
                            <RouterLink :to="{ name: 'course', params: { courseId: course.id } }">
                                <Button
                                    :icon="PrimeIcons.ARROW_RIGHT"
                                    :label="t('components.card.open')"
                                    icon-pos="right"
                                    outlined
                                />
                            </RouterLink>
                        </slot>
                    </template>
                </CourseDetailCard>
            </div>
        </template>
        <template v-else>
            <div class="w-30rem text-center mx-auto">
                <span class="pi pi-exclamation-circle text-6xl text-primary" />
                <slot name="empty">
                    <p>{{ t('components.list.noCourses.student') }}</p>
                    <RouterLink id="courses" :to="{ name: 'courses' }">
                        <Button :label="t('components.button.searchCourse')" icon="pi pi-search" />
                    </RouterLink>
                </slot>
            </div>
        </template>
    </div>
</template>

<style scoped lang="scss"></style>

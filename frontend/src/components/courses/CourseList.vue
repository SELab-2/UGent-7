<script setup lang="ts">
import Skeleton from 'primevue/skeleton';
import CourseDetailCard from '@/components/courses/CourseDetailCard.vue';
import CourseGeneralCard from '@/components/courses/CourseGeneralCard.vue';
import { type Course } from '@/types/Course.ts';
import { useI18n } from 'vue-i18n';
import { PrimeIcons } from 'primevue/api';
import Button from 'primevue/button';

/* Props */
interface Props {
    detail?: boolean;
    courses: Course[] | null;
    cols?: number;
}

withDefaults(defineProps<Props>(), {
    cols: 4,
    detail: true,
});

/* Composable injections */
const { t } = useI18n();
</script>

<template>
    <div class="grid align-items-stretch">
        <template v-if="courses !== null">
            <template v-if="courses.length > 0">
                <div class="col-12 md:col-6" :class="'xl:col-' + 12 / cols" v-for="course in courses" :key="course.id">
                    <CourseDetailCard :course="course" v-if="detail">
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
                    <CourseGeneralCard class="h-full" :course="course" v-else />
                </div>
            </template>
            <template v-else>
                <div class="col-12">
                    <p class="mt-0">{{ t('views.dashboard.no_courses') }}</p>
                </div>
            </template>
        </template>
        <template v-else>
            <div class="col-12 md:col-6 lg:col-4" :class="'xl:col-' + 12 / cols" v-for="index in cols" :key="index">
                <Skeleton :height="detail ? '25rem' : '10rem'" />
            </div>
        </template>
    </div>
</template>

<style scoped lang="scss"></style>

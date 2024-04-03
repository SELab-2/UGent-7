<script setup lang="ts">
import { type Course } from '@/types/Course.ts';
import CourseCard from '@/components/courses/CourseCard.vue';
import Skeleton from 'primevue/skeleton';
import { useI18n } from 'vue-i18n';

/* Props */
defineProps<{ courses: Course[] | null }>();

/* Composable injections */
const { t } = useI18n();
</script>

<template>
    <div class="grid align-items-stretch">
        <template v-if="courses !== null">
            <template v-if="courses.length > 0">
                <div class="col-12 md:col-6 lg:col-4 xl:col-3" v-for="course in courses" :key="course.id">
                    <CourseCard class="h-100" :course="course" />
                </div>
            </template>
            <template v-else>
                <div class="col-12">
                    <p>{{ t('views.dashboard.no_courses') }}</p>
                </div>
            </template>
        </template>
        <template v-else>
            <div class="col-12 md:col-6 lg:col-4 xl:col-3" v-for="index in 4" :key="index">
                <Skeleton height="25rem" style="visibility: hidden" />
            </div>
        </template>
    </div>
</template>

<style scoped lang="scss"></style>

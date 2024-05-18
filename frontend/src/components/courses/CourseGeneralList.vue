<script setup lang="ts">
import CourseGeneralCard from '@/components/courses/CourseGeneralCard.vue';
import Skeleton from 'primevue/skeleton';
import Button from 'primevue/button';
import { type Course } from '@/types/Course.ts';
import { useI18n } from 'vue-i18n';

/* Props */
withDefaults(
    defineProps<{
        cols?: number;
        courses: Course[] | null;
        userCourses: Course[] | null;
    }>(),
    {
        cols: 3,
    },
);

/* Emits */
const emit = defineEmits(['update:courses']);

/* Composable injections */
const { t } = useI18n();
</script>

<template>
    <div class="grid align-items-stretch">
        <template v-if="courses !== null">
            <template v-if="courses.length > 0">
                <div class="col-12 md:col-6" :class="'xl:col-' + 12 / cols" v-for="course in courses" :key="course.id">
                    <CourseGeneralCard
                        class="h-full"
                        :course="course"
                        :courses="userCourses ?? []"
                        @update:courses="emit('update:courses')"
                    />
                </div>
            </template>
            <template v-else>
                <div class="w-30rem text-center mx-auto">
                    <span class="pi pi-exclamation-circle text-6xl text-primary" />
                    <slot name="empty">
                        <p>{{ t('components.list.noCourses') }}</p>
                        <RouterLink :to="{ name: 'courses' }">
                            <Button :label="t('components.button.searchCourse')" icon="pi pi-search" />
                        </RouterLink>
                    </slot>
                </div>
            </template>
        </template>
        <template v-else>
            <div class="col-12 md:col-6 lg:col-4" :class="'xl:col-' + 12 / cols" v-for="index in cols" :key="index">
                <Skeleton height="10rem" />
            </div>
        </template>
    </div>
</template>

<style scoped lang="scss"></style>

<script setup lang="ts">
import Skeleton from 'primevue/skeleton';
import CourseDetailCard from '@/components/courses/CourseDetailCard.vue';
import CourseGeneralCard from '@/components/courses/CourseGeneralCard.vue';
import { type Course } from '@/types/Course.ts';
import { useI18n } from 'vue-i18n';
import { PrimeIcons } from 'primevue/api';
import Button from 'primevue/button';
import { useCourses } from '@/composables/services/course.service.ts';
import { storeToRefs } from 'pinia';
import { useAuthStore } from '@/store/authentication.store.ts';
import { watch } from 'vue';

/* Props */
interface Props {
    detail?: boolean;
    cols?: number;
    courses: Course[] | null;
}

withDefaults(defineProps<Props>(), {
    cols: 4,
    detail: true,
});

/* Composable injections */
const courseService = useCourses();
const { t } = useI18n();
const { user } = storeToRefs(useAuthStore());

/* State */
const userCourses = courseService.courses;

/**
 * Load the courses based on the user role.
 */
async function loadCourses(): Promise<void> {
    if (user.value !== null) {
        if (user.value.isStudent()) {
            await courseService.getCoursesByStudent(user.value.id);
        } else if (user.value.isAssistant()) {
            await courseService.getCourseByAssistant(user.value.id);
        } else if (user.value.isTeacher()) {
            await courseService.getCoursesByTeacher(user.value.id);
        }
    }
}

watch(user, loadCourses, { immediate: true });
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
                    <CourseGeneralCard
                        class="h-full"
                        :course="course"
                        :courses="userCourses ?? []"
                        @update:courses="null"
                        v-else
                    />
                </div>
            </template>
            <template v-else>
                <div class="w-30rem text-center mx-auto">
                    <span class="pi pi-exclamation-circle text-6xl text-primary"/>
                    <p>{{ t('views.dashboard.noCourses') }}</p>
                    <RouterLink :to="{ name: 'courses' }" v-if="user?.isStudent()">
                        <Button :label="t('components.button.searchCourse')" icon="pi pi-search"/>
                    </RouterLink>
                    <RouterLink :to="{ name: 'course-create' }" v-else>
                        <Button :label="t('components.button.createCourse')" icon="pi pi-plus"/>
                    </RouterLink>
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

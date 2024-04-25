<script setup lang="ts">
import CourseGeneralCard from '@/components/courses/CourseGeneralCard.vue';
import Skeleton from 'primevue/skeleton';
import { storeToRefs } from 'pinia';
import { useAuthStore } from '@/store/authentication.store.ts';
import { watch } from 'vue';
import { useCourses } from '@/composables/services/course.service.ts';
import { type Course } from '@/types/Course.ts';
import { useI18n } from 'vue-i18n';

/* Props */
interface Props {
    cols?: number;
    courses: Course[] | null;
}

withDefaults(defineProps<Props>(), {
    cols: 4,
});

/* Composable injections */
const { t } = useI18n();
const { user } = storeToRefs(useAuthStore());
const courseService = useCourses();

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
                    <CourseGeneralCard
                        class="h-full"
                        :course="course"
                        :courses="userCourses ?? []"
                        @update:courses="loadCourses"
                    />
                </div>
            </template>
            <template v-else>
                <div class="w-30rem text-center mx-auto">
                    <span class="pi pi-exclamation-circle text-6xl text-primary" />
                    <p>{{ t('views.dashboard.noCourses') }}</p>
                    <RouterLink :to="{ name: 'courses' }" v-if="user?.isStudent()">
                        <Button :label="t('components.button.searchCourse')" icon="pi pi-search" />
                    </RouterLink>
                    <RouterLink :to="{ name: 'course-create' }" v-else>
                        <Button :label="t('components.button.createCourse')" icon="pi pi-plus" />
                    </RouterLink>
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

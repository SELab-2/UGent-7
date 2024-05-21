<script setup lang="ts">
import CourseForm from '@/components/courses/CourseForm.vue';
import Title from '@/components/layout/Title.vue';
import BaseLayout from '@/components/layout/base/BaseLayout.vue';
import Loading from '@/components/Loading.vue';
import { useI18n } from 'vue-i18n';
import { onMounted, ref } from 'vue';
import { useFaculty } from '@/composables/services/faculty.service.ts';
import { type Course } from '@/types/Course.ts';
import { useCourses } from '@/composables/services/course.service.ts';
import { useRouter } from 'vue-router';

/* Composable injections */
const { t } = useI18n();
const { push } = useRouter();
const { faculties, getFaculties } = useFaculty();
const { createCourse } = useCourses();

/* State */
const loading = ref(true);

/**
 * Save the course.
 *
 * @param course
 */
async function saveCourse(course: Course): Promise<void> {
    await createCourse(course);
    await push({ name: 'dashboard' });
}

/** Load the data */
onMounted(async () => {
    loading.value = true;
    await getFaculties();
    loading.value = false;
});
</script>

<template>
    <BaseLayout>
        <!-- Create course heading -->
        <Title class="mb-6">{{ t('views.courses.create') }}</Title>
        <template v-if="!loading">
            <div class="grid fadein">
                <div class="col-12 md:col-6">
                    <!-- Course form -->
                    <template v-if="faculties !== null">
                        <CourseForm :faculties="faculties" @update:course="saveCourse" />
                    </template>
                </div>
            </div>
        </template>
        <template v-else>
            <Loading height="70vh" />
        </template>
    </BaseLayout>
</template>

<style scoped></style>

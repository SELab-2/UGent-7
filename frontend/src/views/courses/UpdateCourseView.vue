<script setup lang="ts">
import BaseLayout from '@/views/layout/base/BaseLayout.vue';
import CourseForm from '@/components/courses/CourseForm.vue';
import Title from '@/views/layout/Title.vue';
import Loading from '@/components/Loading.vue';
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useCourses } from '@/composables/services/course.service';
import { useFaculty } from '@/composables/services/faculty.service.ts';
import { type Course } from '@/types/Course.ts';
import { watchImmediate } from '@vueuse/core';

/* Composable injections */
const { t } = useI18n();
const { params } = useRoute();
const { push } = useRouter();
const { faculties, getFaculties } = useFaculty();
const { course, getCourseByID, updateCourse } = useCourses();

/* State */
const loading = ref(true);

/**
 * Save the course.
 *
 * @param course
 */
async function saveCourse(course: Course): Promise<void> {
    await updateCourse(course);
    await push({ name: 'course', params: { courseId: course.id } });
}

/* Load course data */
watchImmediate(
    () => params.courseId.toString(),
    async (courseId: string): Promise<void> => {
        loading.value = true;
        await getCourseByID(courseId);
        await getFaculties();
        loading.value = false;
    },
);
</script>

<template>
    <BaseLayout>
        <!-- Create course heading -->
        <Title>{{ t('views.courses.edit') }}</Title>
        <template v-if="!loading">
            <div class="grid fadein">
                <div class="col-12 md:col-6">
                    <!-- Course form -->
                    <template v-if="course !== null && faculties !== null">
                        <CourseForm :course="course" :faculties="faculties" @update:course="saveCourse" />
                    </template>
                </div>
            </div>
        </template>
        <template v-else>
            <Loading height="70vh" />
        </template>
    </BaseLayout>
</template>

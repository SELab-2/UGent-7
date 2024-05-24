<script setup lang="ts">
import CourseForm from '@/components/courses/CourseForm.vue';
import Title from '@/views/layout/Title.vue';
import BaseLayout from '@/views/layout/base/BaseLayout.vue';
import Loading from '@/components/Loading.vue';
import { useI18n } from 'vue-i18n';
import { onMounted, ref } from 'vue';
import { useFaculty } from '@/composables/services/faculty.service.ts';
import { type Course } from '@/types/Course.ts';
import { useCourses } from '@/composables/services/course.service.ts';
import { useRouter } from 'vue-router';
import { useMessagesStore } from '@/store/messages.store.ts';

/* Composable injections */
const { t } = useI18n();
const { addSuccessMessage, addErrorMessage } = useMessagesStore();
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
    try {
        await createCourse(course, false);
        addSuccessMessage(t('toasts.messages.success'), t('toasts.messages.courses.create.success', [course.name]));
        await push({ name: 'dashboard' });
    } catch (error: any) {
        addErrorMessage(t('toasts.messages.error'), t('toasts.messages.courses.create.error', [course.name]));
    }
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
        <Title>{{ t('views.courses.create') }}</Title>
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

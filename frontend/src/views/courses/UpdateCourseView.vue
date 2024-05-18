<script setup lang="ts">
import BaseLayout from '@/components/layout/base/BaseLayout.vue';
import CourseForm from '@/components/courses/CourseForm.vue';
import Skeleton from 'primevue/skeleton';
import Title from '@/components/layout/Title.vue';
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useCourses } from '@/composables/services/course.service';

/* Composable injections */
const { t } = useI18n();
const { params } = useRoute();
const { course, getCourseByID } = useCourses();

/* Load course data */
onMounted(async () => {
    await getCourseByID(params.courseId as string);
});
</script>

<template>
    <BaseLayout>
        <div class="grid fadein">
            <div class="col-12 md:col-6">
                <!-- Create course heading -->
                <Title class="mb-6">{{ t('views.courses.edit') }}</Title>

                <!-- Course form -->
                <CourseForm :course="course" v-if="course !== null" />
                <Skeleton height="100rem" v-else />
            </div>
        </div>
    </BaseLayout>
</template>

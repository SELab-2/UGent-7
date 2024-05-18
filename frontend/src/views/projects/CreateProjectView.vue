<script setup lang="ts">
import BaseLayout from '@/components/layout/base/BaseLayout.vue';
import Title from '@/components/layout/Title.vue';
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useCourses } from '@/composables/services/course.service';
import ProjectForm from '@/components/projects/ProjectForm.vue';

/* Composable injections */
const { t } = useI18n();
const { params } = useRoute();

/* Service injection */
const { course, getCourseByID } = useCourses();

/* Load course data */
onMounted(async () => {
    await getCourseByID(params.courseId as string);
});
</script>

<template>
    <BaseLayout>
        <!-- Create project heading -->
        <Title class="mb-6">
            {{ t('views.projects.create') }}
        </Title>

        <!-- Project form -->
        <ProjectForm :course="course" v-if="course !== null" />
    </BaseLayout>
</template>

<style scoped></style>

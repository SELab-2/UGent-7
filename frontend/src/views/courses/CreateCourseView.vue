<script setup lang="ts">
import CourseForm from '@/components/courses/CourseForm.vue';
import Title from '@/components/layout/Title.vue';
import BaseLayout from '@/components/layout/base/BaseLayout.vue';
import { useI18n } from 'vue-i18n';

/* Composable injections */
const { t } = useI18n();
</script>

<template>
    <BaseLayout>
        <div class="grid fadein">
            <div class="col-12 md:col-6">
                <!-- Create course heading -->
                <Title class="mb-6">{{ t('views.courses.create') }}</Title>

                <!-- Course form -->
                <CourseForm />
            </div>
        </div>
    </BaseLayout>
</template>

<style scoped></style>

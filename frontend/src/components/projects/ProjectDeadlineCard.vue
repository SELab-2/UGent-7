<script setup lang="ts">
import { type Project } from '@/types/Project.ts';
import { type Course } from '@/types/Course.ts';
import { useI18n } from 'vue-i18n';

/* Props */
defineProps<{
    project: Project;
    course: Course;
}>();

/* Composable injections */
const { t } = useI18n();
</script>

<template>
    <RouterLink
        class="text-color"
        :to="{
            name: 'course-project',
            params: {
                courseId: course.id,
                projectId: project.id,
            },
        }"
    >
        <div class="p-5 surface-300 border-round">
            <div class="flex align-items-center gap-5">
                <i class="pi pi-clock text-6xl text-primary" />
                <div class="w-full">
                    <h3 class="m-0">{{ project.name }}</h3>
                    <div class="flex justify-content-between align-items-center mt-2">
                        <span>{{ project.getFormattedDeadline() }}</span>
                        <span v-if="project.getDaysLeft() >= 0">
                            {{
                                t(
                                    'views.projects.days',
                                    { hour: project.getFormattedDeadlineHour() },
                                    project.getDaysLeft(),
                                )
                            }}
                        </span>
                        <span v-else>
                            {{ t('views.projects.ago', project.getDaysLeft() * -1) }}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </RouterLink>
</template>

<style scoped lang="scss"></style>

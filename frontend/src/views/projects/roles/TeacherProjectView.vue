<script setup lang="ts">
import Button from 'primevue/button';
import { Project } from '@/types/Project';
import { Course } from '@/types/Course';
import { PrimeIcons } from 'primevue/api';
import { useI18n } from 'vue-i18n';

const props = defineProps<{
    course: Course;
    project: Project;
}>();

const { t } = useI18n();

</script>

<template>
    <!-- Update course button -->
    <div v-tooltip.top="t('views.courses.edit')">
        <RouterLink :to="{ name: 'project-edit', params: { courseId: props.course.id, projectId: props.project.id } }">
            <Button
                :icon="PrimeIcons.PENCIL"
                icon-pos="right"
                class="custom-button"
                style="height: 51px; width: 51px; margin-right: 10px"
            />
        </RouterLink>
    </div>
</template>

<style scoped lang="scss"></style>

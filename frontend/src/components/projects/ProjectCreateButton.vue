<script setup lang="ts">
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import { useI18n } from 'vue-i18n';
import { type Course } from '@/types/Course.ts';
import { PrimeIcons } from 'primevue/api';
import { ref } from 'vue';
import CourseList from '@/components/courses/CourseList.vue';

/* Composable injections */
const { t } = useI18n();

/* Props */
const props = defineProps<{ courses: Course[]; label?: string; severity?: string }>();

/* Dialog state to select the course you want to create a project for */
const displayCourseSelection = ref(false);
</script>

<template>
    <div>
        <!-- Button to create a new project -->
        <Button
            v-if="props.courses && props.courses.length > 0"
            :icon="PrimeIcons.PLUS"
            icon-pos="right"
            :label="label ?? ''"
            :severity="severity ?? 'primary'"
            class="custom-button"
            @click="displayCourseSelection = true"
        />
        <!-- Dialog to select the course you want to create a project for -->
        <Dialog
            v-model:visible="displayCourseSelection"
            class="m-3"
            :draggable="false"
            :contentStyle="{ 'min-width': '50vw', 'max-width': '1080px' }"
            modal
        >
            <template #header>
                <h2 class="my-3 text-primary">
                    {{ t('views.dashboard.select_course') }}
                </h2>
            </template>
            <template #default>
                <!-- List of courses to select from-->
                <CourseList :cols="3" :courses="props.courses">
                    <template #footer="{ course }">
                        <RouterLink :to="{ name: 'project-create', params: { courseId: course.id } }">
                            <Button
                                :icon="PrimeIcons.PLUS"
                                :label="t('components.card.newProject')"
                                icon-pos="right"
                                outlined
                            />
                        </RouterLink>
                    </template>
                </CourseList>
            </template>
        </Dialog>
    </div>
</template>

<style scoped lang="scss"></style>

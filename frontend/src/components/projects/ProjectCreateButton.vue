<script setup lang="ts">
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import { useI18n } from 'vue-i18n';
import { type Course } from '@/types/Course.ts';
import { PrimeIcons } from 'primevue/api';
import { ref } from 'vue';
import CourseList from '@/components/courses/CourseList.vue';
import { useRouter } from 'vue-router';

/* Composable injections */
const { t } = useI18n();
const { push } = useRouter();

/* Props */
const props = defineProps<{ courses: Course[]; label?: string; severity?: string }>();

/* Dialog state to select the course you want to create a project for */
const displayCourseSelection = ref(false);

/* Method that handles the click on the create button. Displays the dialog if more than 1 course available,
otherwise directly routes to the create page for the given course. */
const handleCreateButton = (): void => {
    // If more then 1 course available, display the dialog
    if (props.courses.length > 1) {
        displayCourseSelection.value = true;
    } else if (props.courses.length === 1) {
        // Only one course available, directly route to the project creation view
        push({ name: 'project-create', params: { courseId: props.courses[0].id } });
    }
};
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
            @click="handleCreateButton"
        />
        <!-- Dialog to select the course you want to create a project for -->
        <Dialog
            v-model:visible="displayCourseSelection"
            class="m-3"
            :draggable="false"
            :contentStyle="{ 'min-width': '50vw' }"
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

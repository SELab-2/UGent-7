<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { type Course } from '@/types/Course.ts';
import { PrimeIcons } from 'primevue/api';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import { useRouter } from 'vue-router';
import { ref } from 'vue';

/* Composable injections */
const { t } = useI18n();
const { push } = useRouter();

/* Props */
const props = defineProps<{ courses: Course[] }>();

/* Dialog state to select the course you want to create a project for */
const displayCourseSelection = ref(false);

/* Method that handles the click on the create button. Displays the dialog if more than 1 course available,
otherwise directly routes to the create page for the given course. */
const handleCreateButton = (): void => {
    // If more then 1 course available, display the dialog
    if (props.courses && props.courses.length > 1) {
        displayCourseSelection.value = true;
    } else if (props.courses && props.courses.length === 1) {
        // Only one course available, directly route to the project creation view
        createProjectForCourse(props.courses[0].id);
    }
};

/* Method to route to the project creation view */
const createProjectForCourse = (courseId: string): void => {
    push({ name: 'project-create', params: { courseId } });
    displayCourseSelection.value = false;
};
</script>

<template>
    <!-- Button to create a new project -->
    <Button
        v-if="props.courses && props.courses.length > 0"
        :icon="PrimeIcons.PLUS"
        icon-pos="right"
        class="custom-button"
        @click="handleCreateButton"
    />
    <!-- Dialog to select the course you want to create a project for -->
    <Dialog
        v-model:visible="displayCourseSelection"
        modal
        :draggable="false"
        :contentStyle="{ width: '50vw' }"
        :header="t('views.dashboard.select_course')"
    >
        <!-- List of courses to select from-->
        <div v-if="props.courses && props.courses.length > 0">
            <div
                v-for="course in props.courses"
                :key="course.id"
                class="course-item"
                @click="createProjectForCourse(course.id)"
            >
                <span class="course-name">{{ course.name }}</span>
            </div>
        </div>
    </Dialog>
</template>

<style scoped lang="scss">
.course-item {
    cursor: pointer;
    padding: 8px;
    border-radius: 4px;
    margin-bottom: 8px;
    transition: background-color 0.3s;
}
.course-item:hover {
    background-color: #f0f0f0;
}
.course-name {
    font-weight: bold;
}
</style>

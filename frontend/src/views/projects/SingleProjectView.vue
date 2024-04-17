<script setup lang="ts">
import BaseLayout from '@/components/layout/base/BaseLayout.vue';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';
import { useRoute } from 'vue-router';
import { type Student } from '@/types/users/Student';
import { type Teacher } from '@/types/users/Teacher';
import { type Assistant } from '@/types/users/Assistant';
import StudentProjectView from '@/views/projects/roles/StudentProjectView.vue';
import TeacherProjectView from '@/views/projects/roles/TeacherProjectView.vue';
import AssistantProjectView from '@/views/projects/roles/AssistantProjectView.vue';
import { onMounted } from 'vue';
import { useCourses } from '@/composables/services/course.service';
import { useProject } from '@/composables/services/project.service';

/* Service injection */
const { user } = storeToRefs(useAuthStore());
const { params } = useRoute();
const { project, getProjectByID } = useProject();
const { course, getCourseByID } = useCourses();

onMounted(async () => {
    await getProjectByID(params.projectId as string);
    await getCourseByID(params.courseId as string);
});

</script>

<template>
    <BaseLayout>
        <StudentProjectView v-if="user?.isStudent()" :student="user as Student" />
        <TeacherProjectView v-else-if="user?.isTeacher() && project && course" :teacher="user as Teacher" :project="project" :course = "course" />
        <AssistantProjectView v-else-if="user?.isAssistant()" :assistant="user as Assistant" />
    </BaseLayout>
</template>

<style scoped></style>

<script setup lang="ts">
import StudentProjectView from '@/views/projects/roles/StudentProjectView.vue';
import TeacherProjectView from '@/views/projects/roles/TeacherProjectView.vue';
import AssistantProjectView from '@/views/projects/roles/AssistantProjectView.vue';
import BaseLayout from '@/components/layout/base/BaseLayout.vue';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';
import { type Student } from '@/types/users/Student';
import { type Teacher } from '@/types/users/Teacher';
import { type Assistant } from '@/types/users/Assistant';
import { useProject } from '@/composables/services/project.service.ts';
import { useRoute } from 'vue-router';
import { watch } from 'vue';
import { useGroup } from '@/composables/services/group.service.ts';
import { useStudents } from '@/composables/services/student.service.ts';

/* Service injection */
const { params } = useRoute();
const { user } = storeToRefs(useAuthStore());
const { project, getProjectByID } = useProject();
const { groups, getGroupsByProject } = useGroup();
const { students, getStudentsByGroup } = useStudents();

/* Watch the query parameters for changes */
watch(() => params, async (params) => {
    const projectId = params.projectId as string;

    if (projectId) {
        // Get the project by the ID param.
        await getProjectByID(projectId);

        // Get the groups of the project.
        await getGroupsByProject(projectId);

        if (project.value !== null && groups.value !== null) {
            project.value.groups = groups.value;

            // Fill the students with each group.
            for (const group of groups.value) {
                await getStudentsByGroup(group.id);
                group.students = students.value ?? [];
                group.project = project.value;
            }
        }
    }
}, {
    immediate: true
});
</script>

<template>
    <BaseLayout>
        <StudentProjectView v-if="user?.isStudent()" :student="user as Student" :project="project" />
        <TeacherProjectView v-else-if="user?.isTeacher()" :teacher="user as Teacher" :project="project" />
        <AssistantProjectView v-else-if="user?.isAssistant()" :assistant="user as Assistant" :project="project" />
    </BaseLayout>
</template>

<style scoped></style>

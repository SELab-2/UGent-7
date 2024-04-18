<script setup lang="ts">
import ChooseGroupCard from '@/components/projects/ChooseGroupCard.vue';
import JoinedGroupCard from '@/components/projects/JoinedGroupCard.vue';
import SubmissionCard from '@/components/projects/SubmissionCard.vue';
import ProjectInfo from '@/components/projects/ProjectInfo.vue';
import Title from '@/components/layout/Title.vue';
import Skeleton from 'primevue/skeleton';
import { ref, watch } from 'vue';
import { useProject } from '@/composables/services/project.service.ts';
import { useRoute } from 'vue-router';
import { useGroup } from '@/composables/services/group.service.ts';
import { type Group } from '@/types/Group.ts';
import { type Student } from '@/types/users/Student.ts';
import { useStudents } from '@/composables/services/student.service.ts';

/* Props */
const props = defineProps<{
    student: Student;
}>();

/* Composable injections */
const route = useRoute();
const { project, getProjectByID } = useProject();
const { groups, getGroupsByProject, getGroupsByStudent } = useGroup();
const { students, getStudentsByGroup } = useStudents();

/* Component state */
const studentGroup = ref<Group | undefined | null>(undefined);

/**
 * Handles the group changed event.
 */
async function handleGroupChanged(): Promise<void> {
    await loadData();
}

watch(() => [props.student, route.params.projectId], loadData, {
    immediate: true,
});

/**
 * Loads the data for the project view.
 */
async function loadData(): Promise<void> {
    studentGroup.value = undefined;
    const projectId = route.params.projectId as string;

    // Get the project by the ID param.
    await getProjectByID(projectId);

    // Get the groups of the project.
    await getGroupsByProject(projectId);

    if (project.value !== null) {
        project.value.groups = groups.value ?? [];
    }

    for (const group of project.value?.groups ?? []) {
        await getStudentsByGroup(group.id);
        group.students = students.value ?? [];
        group.project = project.value;
    }

    // Get the group of the student for this project.
    await getGroupsByStudent(props.student.id);
    studentGroup.value =
        project.value?.groups?.find((group) => groups.value?.some((projectGroup) => projectGroup.id === group.id)) ??
        null;
}
</script>

<template>
    <template v-if="project !== null">
        <Title class="mb-4">
            {{ project.name }}
        </Title>
    </template>
    <template v-else>
        <Skeleton class="mb-4" height="3rem" width="30rem" />
    </template>
    <div class="grid">
        <div class="col-12 md:col-8">
            <template v-if="project !== null">
                <ProjectInfo class="my-3" :project="project" />
                <div v-if="project" v-html="project.description" />
            </template>
            <template v-else>
                <Skeleton height="4rem" />
                <Skeleton height="10rem" />
            </template>
        </div>
        <div class="col-12 md:col-4">
            <template v-if="project !== null">
                <div class="mt-3">
                    <template v-if="studentGroup === null">
                        <ChooseGroupCard :project="project" :student="student" @group-joined="handleGroupChanged" />
                    </template>
                    <template v-else-if="studentGroup !== undefined">
                        <SubmissionCard class="mb-3" :group="studentGroup" />
                        <JoinedGroupCard :group="studentGroup" @group-left="handleGroupChanged"></JoinedGroupCard>
                    </template>
                    <template v-else>
                        <Skeleton height="30rem" />
                        <Skeleton height="10rem" class="mt-3" />
                    </template>
                </div>
            </template>
            <template v-else>
                <Skeleton height="30rem" />
                <Skeleton height="10rem" class="mt-3" />
            </template>
        </div>
    </div>
</template>

<style scoped lang="scss"></style>

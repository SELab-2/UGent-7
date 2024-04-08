<script setup lang="ts">
import ChooseGroupCard from '@/components/projects/ChooseGroupCard.vue';
import JoinedGroupCard from '@/components/projects/JoinedGroupCard.vue';
import Title from '@/components/layout/Title.vue';
import Skeleton from 'primevue/skeleton';
import { onMounted, ref } from 'vue';
import { useProject } from '@/composables/services/project.service.ts';
import { useRoute } from 'vue-router';
import { useGroup } from '@/composables/services/groups.service.ts';
import { type Group } from '@/types/Group.ts';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';
import { type Student } from '@/types/users/Student.ts';
import SubmissionCard from '@/components/projects/SubmissionCard.vue';

/* Composable injections */
const route = useRoute();
const { student } = storeToRefs(useAuthStore());
const { project, getProjectByID } = useProject();
const { groups, getGroupsByProject, getGroupsByStudent } = useGroup();

/* Component state */
const group = ref<Group | null>(null);
const projectGroups = ref<Group[]>([]);

/**
 * Handles the group changed event.
 *
 * @param joinedGroupData
 */
function handleGroupChanged(joinedGroupData: Group): void {
    group.value = joinedGroupData;
}

onMounted(async () => {
    if (student.value !== null) {
        const currentStudent: Student = student.value;
        const projectId: string = route.params.projectId as string;

        await getProjectByID(projectId);
        await getGroupsByProject(projectId);
        projectGroups.value = groups.value ?? [];

        // Check if the student is in a group for the project
        await getGroupsByStudent(currentStudent.id.toString());

        group.value =
            groups.value?.find((group) => projectGroups.value?.some((projectGroup) => projectGroup.id === group.id)) ??
            null;
    }
});
</script>

<template>
    <div class="grid">
        <div class="col-12 md:col-9">
            <div>
                <Title v-if="project">
                    {{ project.name }}
                </Title>
                <Skeleton class="mb-4" height="3rem" width="30rem" v-else />
            </div>
            <div>
                <p v-if="project">
                    {{ project.description }}
                </p>
                <Skeleton height="10rem" v-else />
            </div>
        </div>
        <div class="col-12 md:col-3">
            <SubmissionCard v-if="group && project" :project="project" :group="group" />
            <JoinedGroupCard v-if="group" :group="group" @group-left="handleGroupChanged"></JoinedGroupCard>
            <ChooseGroupCard v-else :groups="projectGroups" @group-joined="handleGroupChanged"></ChooseGroupCard>
        </div>
    </div>
</template>

<style scoped lang="scss"></style>

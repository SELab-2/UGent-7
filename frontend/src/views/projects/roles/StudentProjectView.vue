<script setup lang="ts">
import ChooseGroupCard from '@/components/projects/ChooseGroupCard.vue';
import JoinedGroupCard from '@/components/projects/JoinedGroupCard.vue';
import SubmissionCard from '@/components/projects/SubmissionCard.vue';
import ProjectInfo from '@/components/projects/ProjectInfo.vue';
import Title from '@/components/layout/Title.vue';
import Skeleton from 'primevue/skeleton';
import { computed, watch } from 'vue';
import { useGroup } from '@/composables/services/group.service.ts';
import { type Group } from '@/types/Group.ts';
import { type Student } from '@/types/users/Student.ts';
import { type Project } from '@/types/Project.ts';

/* Props */
const props = defineProps<{
    student: Student;
    project: Project | null;
}>();

/* Composable injections */
const { groups, getGroupsByStudent } = useGroup();

/* Component state */
const group = computed(() => {
    if (groups.value !== null && props.project !== null) {
        const studentGroups = groups.value;

        if (studentGroups !== null) {
            return (
                props.project.groups?.find((projectGroup: Group) =>
                    studentGroups.some((studentGroup: Group) => studentGroup.id === projectGroup.id),
                ) ?? null
            );
        }

        return null;
    }

    return undefined;
});

/* Watch the student and project ID for changes */
watch(() => [props.student], loadStudentGroups, {
    immediate: true,
});

/**
 * Loads the data for the project view.
 */
async function loadStudentGroups(): Promise<void> {
    // Get the groups of the given student.
    await getGroupsByStudent(props.student.id);
}
</script>

<template>
    <template v-if="project !== null">
        <Title class="mb-5">
            {{ project.name }}
        </Title>
    </template>
    <template v-else>
        <Skeleton class="mb-4" height="3rem" width="30rem" />
    </template>
    <div class="grid">
        <div class="col-12 md:col-8">
            <template v-if="project !== null">
                <ProjectInfo class="mb-3" :project="project" />
                <div v-if="project" v-html="project.description" />
            </template>
            <template v-else>
                <Skeleton height="4rem" class="mb-3" />
                <Skeleton height="10rem" />
            </template>
        </div>
        <div class="col-12 md:col-4">
            <template v-if="project !== null && group !== undefined">
                <template v-if="group === null">
                    <ChooseGroupCard :project="project" :student="student" @group-joined="loadStudentGroups" />
                </template>
                <template v-else>
                    <SubmissionCard class="mb-3" :group="group" />
                    <JoinedGroupCard
                        v-if="project.group_size !== 1"
                        :group="group"
                        @group-left="loadStudentGroups"
                    ></JoinedGroupCard>
                </template>
            </template>
            <template v-else>
                <Skeleton height="10rem" class="mb-3" />
                <Skeleton height="30rem" />
            </template>
        </div>
    </div>
</template>

<style scoped lang="scss"></style>

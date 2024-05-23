<script setup lang="ts">
import ChooseGroupCard from '@/components/projects/groups/GroupChooseCard.vue';
import JoinedGroupCard from '@/components/projects/groups/GroupJoinedCard.vue';
import SubmissionCard from '@/components/submissions/SubmissionCard.vue';
import ProjectInfo from '@/components/projects/ProjectInfo.vue';
import ProjectStructure from '@/components/projects/ProjectStructure.vue';
import Title from '@/views/layout/Title.vue';
import Loading from '@/components/Loading.vue';
import { ref } from 'vue';
import { useGroup } from '@/composables/services/group.service.ts';
import { type Group } from '@/types/Group.ts';
import { type Student } from '@/types/users/Student.ts';
import { watchImmediate } from '@vueuse/core';
import { useStudents } from '@/composables/services/student.service.ts';
import { useSubmission } from '@/composables/services/submission.service.ts';
import { useProject } from '@/composables/services/project.service.ts';
import { useRoute } from 'vue-router';
import { type Project } from '@/types/Project.ts';
import {useStructureCheck} from "@/composables/services/structure_check.service.ts";

/* Props */
defineProps<{
    student: Student;
}>();

/* Composable injections */
const { params } = useRoute();
const { group, groups, getGroupByStudentProject, getGroupsByProject } = useGroup();
const { students, getStudentsByGroup, studentJoinGroup, studentLeaveGroup } = useStudents();
const { structureChecks, getStructureCheckByProject } = useStructureCheck();
const { project, getProjectByID } = useProject();
const { submissions, getSubmissionByGroup } = useSubmission();

/* State */
const loadingGroup = ref<boolean>(true);

/**
 * Join a group.
 *
 * @param newGroup The group to join.
 * @param student The student joining the group.
 */
async function joinGroup(newGroup: Group, student: Student): Promise<void> {
    await studentJoinGroup(newGroup.id, student.id);

    if (project.value !== null) {
        await getStudentData(project.value);
    }
}

/**
 * Leave a group.
 *
 * @param newGroup The group to leave.
 * @param student The student leaving the group.
 */
async function leaveGroup(newGroup: Group, student: Student): Promise<void> {
    await studentLeaveGroup(newGroup.id, student.id);

    if (project.value !== null) {
        group.value = null;
    }
}

/**
 * Get the student's group.
 *
 * @param project The project to get the group for.
 */
async function getStudentData(project: Project): Promise<void> {
    loadingGroup.value = true;
    await getGroupByStudentProject(project.id);

    if (group.value !== null) {
        // Load the group's submissions.
        await getSubmissionByGroup(group.value.id);

        // Load the group's students.
        await getStudentsByGroup(group.value.id);

        if (students.value !== null) {
            group.value.students = students.value;
        }
    }

    loadingGroup.value = false;
}

/**
 * Get the project's groups.
 *
 * @param project The project to get the groups for.
 */
async function getProjectData(project: Project): Promise<void> {
    await getGroupsByProject(project.id);
    await getStructureCheckByProject(project.id);

    if (groups.value !== null) {
        project.groups = groups.value;
    }
}

/* Load the project groups. */
watchImmediate(
    () => params,
    async () => {
        // Load the project.
        await getProjectByID(params.projectId.toString());

        if (project.value !== null) {
            // Load the student's group.
            await getStudentData(project.value);

            // Load the project's groups.
            await getProjectData(project.value);
        }
    },
);
</script>

<template>
    <template v-if="project !== null">
        <div class="fadein">
            <Title class="mb-5">
                {{ project.name }}
            </Title>
            <div class="grid">
                <div class="col-12 md:col-8">
                    <ProjectInfo class="mb-3" :project="project" />
                    <div v-if="project" v-html="project.description" />
                    <ProjectStructure v-if="structureChecks" :structure-checks="structureChecks"/>
                </div>
                <div class="col-12 md:col-4">
                    <template v-if="!loadingGroup">
                        <template v-if="group === null && groups !== null">
                            <div class="fadein">
                                <ChooseGroupCard
                                    :project="project"
                                    :groups="groups"
                                    :student="student"
                                    @join:group="joinGroup"
                                />
                            </div>
                        </template>
                        <template v-else>
                            <template v-if="submissions !== null && group !== null">
                                <div class="fadein">
                                    <SubmissionCard class="mb-3" :group="group" :submissions="submissions">
                                    </SubmissionCard>
                                    <JoinedGroupCard
                                        v-if="project.group_size !== 1"
                                        :group="group"
                                        @leave:group="leaveGroup"
                                    >
                                    </JoinedGroupCard>
                                </div>
                            </template>
                        </template>
                    </template>
                    <template v-else>
                        <Loading height="70vh" />
                    </template>
                </div>
            </div>
        </div>
    </template>
    <template v-else>
        <Loading height="70vh" />
    </template>
</template>

<style scoped lang="scss"></style>

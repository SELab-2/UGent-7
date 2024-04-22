<script setup lang="ts">
import Title from '@/components/layout/Title.vue';
import Skeleton from 'primevue/skeleton';
import { type Teacher } from '@/types/users/Teacher.ts';
import { type Project } from '@/types/Project.ts';
import ProjectInfo from '@/components/projects/ProjectInfo.vue';
import { useSubmissionStatus } from '@/composables/services/submission_status.service.ts';
import { watch } from 'vue';
import ProjectMeter from '@/components/projects/ProjectMeter.vue';
import StructureCheckTreeView from '@/components/structure_checks/StructureCheckTreeView.vue';

/* Props */
const props = defineProps<{
    teacher: Teacher;
    project: Project | null;
}>();

/* Composable injections */
const { submissionStatus, getSubmissionStatusByProject } = useSubmissionStatus();

/* Watchers */
watch(
    () => props.project,
    () => {
        if (props.project !== null) {
            getSubmissionStatusByProject(props.project.id);
        }
    },
    {
        immediate: true,
    },
);
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
                <Skeleton height="4rem" />
                <Skeleton height="10rem" />
            </template>
        </div>
        <div class="col-12 md:col-4">
            <ProjectMeter :submission-status="submissionStatus" />
        </div>
        <StructureCheckTreeView v-if="props.project" :projectId="`${props.project.id}`"  :editable=false>
        </StructureCheckTreeView>
    </div>
</template>

<style scoped lang="scss"></style>

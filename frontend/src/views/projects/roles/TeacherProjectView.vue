<script setup lang="ts">
import Title from '@/components/layout/Title.vue';
import Skeleton from 'primevue/skeleton';
import { Teacher } from '@/types/users/Teacher.ts';
import { Project } from '@/types/Project.ts';
import ChooseGroupCard from '@/components/projects/ChooseGroupCard.vue';
import ProjectInfo from '@/components/projects/ProjectInfo.vue';
import SubmissionCard from '@/components/projects/SubmissionCard.vue';
import JoinedGroupCard from '@/components/projects/JoinedGroupCard.vue';

/* Props */
const props = defineProps<{
    teacher: Teacher;
    project: Project|null;
}>();

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
            Hellaur
        </div>
    </div>
</template>

<style scoped lang="scss"></style>

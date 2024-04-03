<script setup lang="ts">
import BaseLayout from '@/components/layout/BaseLayout.vue';
import { ref, watch } from 'vue';
import { useProject } from '@/composables/services/project.service.ts';
import { useRoute } from 'vue-router';
import Title from '@/components/layout/Title.vue';
import Skeleton from 'primevue/skeleton';
import GroupCard from '@/components/projects/GroupCard.vue';
import { useGroup } from '@/composables/services/groups.service.ts';
import { type Group } from '@/types/Group.ts';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';

/* Composable injections */
const route = useRoute();
const { student } = storeToRefs(useAuthStore());
const { project, getProjectByID } = useProject();
const { groups, getGroupsByProject, getGroupsByStudent } = useGroup();

/* Component state */
const group = ref<Group | null>(null);

watch(
    student,
    async () => {
        if (student.value !== null) {
            const projectId = route.params.projectId as string;
            await getProjectByID(projectId.toString());
            await getGroupsByProject(projectId.toString());

            // Check if the student is in a group for the project
            const projectGroups = groups.value;
            await getGroupsByStudent('1');

            for (const studentGroup of groups.value ?? []) {
                const isCommonGroup = projectGroups?.some(
                    (projectGroup) => projectGroup.id === studentGroup.id,
                );

                if (isCommonGroup === true) {
                    group.value = studentGroup;
                    break;
                }
            }
        }
    },
    {
        immediate: true,
    },
);
</script>

<template>
    <BaseLayout>
        <div class="grid">
            <div class="col-12 md:col-8">
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
            <div class="col-12 md:col-4">
                <GroupCard :group="group" v-if="group"></GroupCard>

                <Skeleton height="20rem" v-else />
            </div>
        </div>
    </BaseLayout>
</template>

<style scoped lang="scss"></style>

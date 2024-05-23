<script setup lang="ts">
import Title from '@/views/layout/Title.vue';
import Button from 'primevue/button';
import ButtonGroup from 'primevue/buttongroup';
import ProjectInfo from '@/components/projects/ProjectInfo.vue';
import DownloadCSVButton from '@/components/projects/ProjectDownloadGradesButton.vue';
import ProjectMeter from '@/components/submissions/ProjectMeter.vue';
import GroupsManageTable from '@/components/projects/groups/GroupsManageTable.vue';
import Loading from '@/components/Loading.vue';
import { type Teacher } from '@/types/users/Teacher.ts';
import { PrimeIcons } from 'primevue/api';
import { useI18n } from 'vue-i18n';
import { useGroup } from '@/composables/services/group.service.ts';
import { watchImmediate } from '@vueuse/core';
import { useProject } from '@/composables/services/project.service.ts';
import { useRoute } from 'vue-router';
import { useMessagesStore } from '@/store/messages.store.ts';
import { type Group } from '@/types/Group.ts';
import { type Assistant } from '@/types/users/Assistant.ts';
import { processError } from '@/composables/services/helpers.ts';

/* Props */
defineProps<{
    teacher: Teacher | Assistant;
}>();

/* Composables */
const { t } = useI18n();
const { params } = useRoute();
const { addSuccessMessage } = useMessagesStore();
const { project, getProjectByID, updateProject } = useProject();
const { groups, getGroupsByProject, updateGroup } = useGroup();

/**
 * Updates the score of a group.
 *
 * @param group The group to update.
 * @param score The new score.
 */
async function updateGroupScore(group: Group, score: number): Promise<void> {
    try {
        await updateGroup(
            {
                ...group,
                score,
            },
            false,
        );

        group.score = score;

        addSuccessMessage('Gelukt', 'De groepsscore is bijgewerkt.');
    } catch (error) {
        processError(error);
    }
}

/**
 * Publishes the scores of the project.
 */
async function publishScores(): Promise<void> {
    if (project.value !== null) {
        project.value.score_visible = true;

        try {
            await updateProject(project.value);
            addSuccessMessage(t('toasts.messages.success'), t('views.projects.scoresPublished'));
        } catch (error) {
            console.log(error);
        }
    }
}

/* Load the project groups. */
watchImmediate(
    () => params,
    async () => {
        await getProjectByID(params.projectId.toString());

        if (project.value !== null) {
            await getGroupsByProject(project.value.id);

            if (groups.value !== null) {
                project.value.groups = groups.value;
            }
        }
    },
);
</script>

<template>
    <template v-if="project !== null">
        <div class="fadein">
            <div class="flex align-items-center justify-content-between gap-3">
                <Title class="mb-5">
                    {{ project.name }}
                </Title>
                <RouterLink
                    :to="{ name: 'project-edit', params: { courseId: project.course.id, projectId: project.id } }"
                >
                    <Button :label="t('views.projects.edit')" :icon="PrimeIcons.PENCIL"> </Button>
                </RouterLink>
            </div>
            <div class="grid">
                <div class="col-12 md:col-8">
                    <ProjectInfo class="mb-3" :project="project" />
                    <h2>
                        {{ t('views.projects.groups') }}
                    </h2>
                    <template v-if="groups !== null">
                        <div class="fadein">
                            <GroupsManageTable
                                :project="project"
                                :groups="groups"
                                @update:group-score="updateGroupScore"
                            />
                            <ButtonGroup class="flex mt-4">
                                <Button
                                    :icon="PrimeIcons.UPLOAD"
                                    :disabled="project.score_visible"
                                    :label="t('views.projects.publishScores')"
                                    @click="publishScores"
                                />
                                <DownloadCSVButton
                                    :project="project"
                                    :groups="groups"
                                    :icon="PrimeIcons.DOWNLOAD"
                                    outlined
                                />
                            </ButtonGroup>
                        </div>
                    </template>
                    <template v-else>
                        <Loading height="70vh" />
                    </template>
                </div>
                <div class="col-12 md:col-4">
                    <h2 class="mt-0">
                        {{ t('views.projects.submissionStatus') }}
                    </h2>
                    <ProjectMeter :project="project" />
                </div>
            </div>
        </div>
    </template>
    <template v-else>
        <Loading height="70vh" />
    </template>
</template>

<style scoped lang="scss"></style>

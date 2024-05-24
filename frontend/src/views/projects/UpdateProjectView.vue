<script setup lang="ts">
import BaseLayout from '@/views/layout/base/BaseLayout.vue';
import Title from '@/views/layout/Title.vue';
import ProjectForm from '@/components/projects/ProjectForm.vue';
import Loading from '@/components/Loading.vue';
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useProject } from '@/composables/services/project.service';
import { useStructureCheck } from '@/composables/services/structure_check.service.ts';
import { type Project } from '@/types/Project.ts';
import { processError } from '@/composables/services/helpers.ts';
import { useMessagesStore } from '@/store/messages.store.ts';
import { useDockerImages } from '@/composables/services/docker.service.ts';
import { useExtraCheck } from '@/composables/services/extra_checks.service.ts';
import { type DockerImage } from '@/types/DockerImage.ts';
import { type ExtraCheck } from '@/types/ExtraCheck.ts';
import { watchImmediate } from '@vueuse/core';

/* Composable injections */
const { t } = useI18n();
const { params } = useRoute();

/* Service injection */
const { push } = useRouter();
const { addErrorMessage } = useMessagesStore();
const { project, updateProject, getProjectByID } = useProject();
const { structureChecks, setStructureChecks, getStructureCheckByProject } = useStructureCheck();
const { extraChecks, setExtraChecks, deleteExtraCheck, getExtraChecksByProject } = useExtraCheck();
const { dockerImages, getDockerImages, createDockerImage, deleteDockerImage } = useDockerImages();

/* State */
const loading = ref(true);

/**
 * Save the project.
 *
 * @param newProject
 */
async function saveProject(newProject: Project): Promise<void> {
    try {
        if (project.value !== null) {
            await updateProject(newProject);
        } else {
            // Failed to update the project
            addErrorMessage('Onbekende fout', 'Kon het project niet updaten');
        }

        if (project.value !== null) {
            // Set the structure checks.
            await setStructureChecks(newProject.structure_checks ?? [], project.value.id);

            // Set the extra checks.
            await setExtraChecks(newProject.extra_checks ?? [], project.value.id);

            // Delete the deleted checks
            const deletedChecks = project.value.extra_checks.filter(
                (check) =>
                    newProject.extra_checks.find((newCheck: ExtraCheck) => newCheck.id === check.id) === undefined,
            );

            for (const check of deletedChecks) {
                await deleteExtraCheck(check.id);
            }

            // Redirect to the course project page.
            await push({
                name: 'course-project',
                params: { courseId: project.value.course.id, projectId: project.value.id },
            });
        } else {
            // Failed to set the structure checks.
            addErrorMessage('Onbekende fout', 'Kon de structuur van het project niet updaten');
        }
    } catch (error: any) {
        processError(error);
    }
}

/**
 * Save the docker image.
 *
 * @param dockerImage
 * @param file
 */
async function saveDockerImage(dockerImage: DockerImage, file: File): Promise<void> {
    try {
        await createDockerImage(dockerImage, file);
        await getDockerImages();
    } catch (error: any) {
        processError(error);
    }
}

/**
 * Delete the docker image.
 *
 * @param dockerImage
 */
async function removeDockerImage(dockerImage: DockerImage): Promise<void> {
    try {
        await deleteDockerImage(dockerImage.id);
        await getDockerImages();
    } catch (error: any) {
        processError(error);
    }
}

/* Load project data */
watchImmediate(
    () => params.projectId,
    async () => {
        loading.value = true;

        try {
            await getProjectByID(params.projectId.toString());
            await getDockerImages();

            if (project.value !== null) {
                await getStructureCheckByProject(project.value.id);

                if (structureChecks.value !== null) {
                    project.value.structure_checks = structureChecks.value;
                }

                await getExtraChecksByProject(project.value.id);

                if (extraChecks.value !== null) {
                    project.value.extra_checks = extraChecks.value;
                }
            }
        } catch (error: any) {
            processError(error);
        }

        loading.value = false;
    },
);
</script>

<template>
    <BaseLayout>
        <template v-if="!loading">
            <div class="fadein">
                <!-- Update project heading -->
                <Title class="mb-5">
                    {{ t('views.projects.edit') }}
                </Title>

                <!-- Project form -->
                <template v-if="project !== null && dockerImages !== null">
                    <ProjectForm
                        :course="project.course"
                        :project="project"
                        :docker-images="dockerImages"
                        @create:docker-image="saveDockerImage"
                        @delete:docker-image="removeDockerImage"
                        @update:project="saveProject"
                    />
                </template>
            </div>
        </template>
        <template v-else>
            <Loading height="70vh" />
        </template>
    </BaseLayout>
</template>

<style scoped></style>

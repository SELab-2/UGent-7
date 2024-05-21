<script setup lang="ts">
import BaseLayout from '@/components/layout/base/BaseLayout.vue';
import Title from '@/components/layout/Title.vue';
import ProjectForm from '@/components/projects/ProjectForm.vue';
import Loading from '@/components/Loading.vue';
import { onMounted, ref } from 'vue';
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

/* Composable injections */
const { t } = useI18n();
const { params } = useRoute();

/* Service injection */
const { push } = useRouter();
const { addErrorMessage } = useMessagesStore();
const { project, updateProject, getProjectByID } = useProject();
const { structureChecks, setStructureChecks, getStructureCheckByProject } = useStructureCheck();
const { extraChecks, setExtraChecks, deleteExtraCheck, getExtraChecksByProject } = useExtraCheck();
const { dockerImages, getDockerImages, createDockerImage } = useDockerImages();

/* State */
const isLoading = ref(true);

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
            const deletedChecks = (project.value.extra_checks ?? []).filter(
                (check) => !(newProject.extra_checks ?? []).find((newCheck: ExtraCheck) => newCheck.id === check.id),
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

/* Load project data */
onMounted(async () => {
    try {
        await getProjectByID(params.projectId as string);
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

        isLoading.value = false;
    } catch (error: any) {
        processError(error);
    }
});
</script>

<template>
    <BaseLayout>
        <!-- Update project heading -->
        <Title class="mb-6">
            {{ t('views.projects.edit') }}
        </Title>

        <!-- Project form -->
        <template v-if="project !== null && dockerImages !== null && !isLoading">
            <ProjectForm
                :course="project.course"
                :project="project"
                :docker-images="dockerImages"
                @create:docker-image="saveDockerImage"
                @update:project="saveProject"
            />
        </template>
        <template v-else>
            <Loading />
        </template>
    </BaseLayout>
</template>

<style scoped></style>

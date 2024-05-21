<script setup lang="ts">
import BaseLayout from '@/components/layout/base/BaseLayout.vue';
import Title from '@/components/layout/Title.vue';
import ProjectForm from '@/components/projects/ProjectForm.vue';
import { onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useProject } from '@/composables/services/project.service';
import { useStructureCheck } from '@/composables/services/structure_check.service.ts';
import { Project } from '@/types/Project.ts';
import { processError } from '@/composables/services/helpers.ts';
import { useMessagesStore } from '@/store/messages.store.ts';

/* Composable injections */
const { t } = useI18n();
const { params } = useRoute();

/* Service injection */
const { push } = useRouter();
const { addErrorMessage } = useMessagesStore();
const { project, updateProject, getProjectByID } = useProject();
const { structureChecks, setStructureChecks, getStructureCheckByProject } = useStructureCheck();

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
            await setStructureChecks(newProject.structure_checks ?? [], project.value.id);
            await push({ name: 'course-project', params: { courseId: project.value.course.id, projectId: project.value.id } });
        } else {
            // Failed to set the structure checks.
            addErrorMessage('Onbekende fout', 'Kon de structuur van het project niet updaten');
        }
    } catch (error: any) {
        processError(error);
    }
}

/* Load project data */
onMounted(async () => {
    await getProjectByID(params.projectId as string);

    if (project.value !== null) {
        await getStructureCheckByProject(project.value.id);

        if (structureChecks.value !== null) {
            project.value.structure_checks = structureChecks.value;
        }
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
        <ProjectForm :course="project.course" :project="project" v-if="project !== null" @update:project="saveProject" />
    </BaseLayout>
</template>

<style scoped></style>

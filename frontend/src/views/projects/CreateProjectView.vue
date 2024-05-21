<script setup lang="ts">
import BaseLayout from '@/components/layout/base/BaseLayout.vue';
import Title from '@/components/layout/Title.vue';
import { onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useCourses } from '@/composables/services/course.service';
import ProjectForm from '@/components/projects/ProjectForm.vue';
import { type Project } from '@/types/Project.ts';
import { useProject } from '@/composables/services/project.service.ts';
import { processError } from '@/composables/services/helpers.ts';
import { useStructureCheck } from '@/composables/services/structure_check.service.ts';
import { useMessagesStore } from '@/store/messages.store.ts';
import { useDockerImages } from '@/composables/services/docker.service.ts';
import { type DockerImage } from '@/types/DockerImage.ts';
import { useExtraCheck } from '@/composables/services/extra_checks.service.ts';

/* Composable injections */
const { t } = useI18n();
const { params } = useRoute();

/* Service injection */
const { push } = useRouter();
const { addErrorMessage } = useMessagesStore();
const { course, getCourseByID } = useCourses();
const { project, createProject } = useProject();
const { setStructureChecks } = useStructureCheck();
const { setExtraChecks } = useExtraCheck();
const { dockerImages, getDockerImages, createDockerImage } = useDockerImages();

/**
 * Save the project.
 *
 * @param newProject
 * @param numberOfGroups
 */
async function saveProject(newProject: Project, numberOfGroups: number): Promise<void> {
    try {
        if (course.value !== null) {
            await createProject(newProject, course.value.id, numberOfGroups);

            if (project.value !== null) {
                await setStructureChecks(newProject.structure_checks ?? [], project.value.id);
                await setExtraChecks(newProject.extra_checks ?? [], project.value.id);
                await push({
                    name: 'course-project',
                    params: { courseId: course.value.id, projectId: project.value.id },
                });
            }

            addErrorMessage(t('views.projects.create.error'), t('views.projects.create.error_description'));
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

/* Load course data */
onMounted(async () => {
    try {
        await getCourseByID(params.courseId as string);
        await getDockerImages();
    } catch (error: any) {
        processError(error);
    }
});
</script>

<template>
    <BaseLayout>
        <!-- Create project heading -->
        <Title class="mb-6">
            {{ t('views.projects.create') }}
        </Title>

        <!-- Project form -->
        <template v-if="dockerImages !== null && course !== null">
            <ProjectForm
                :course="course"
                :docker-images="dockerImages"
                @update:project="(project, numberOfGroups) => saveProject(project, numberOfGroups)"
                @create:docker-image="saveDockerImage"
            />
        </template>
    </BaseLayout>
</template>

<style scoped></style>

<script setup lang="ts">
import BaseLayout from '@/views/layout/base/BaseLayout.vue';
import Title from '@/views/layout/Title.vue';
import { ref } from 'vue';
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
import Loading from '@/components/Loading.vue';
import { watchImmediate } from '@vueuse/core';

/* Composable injections */
const { t } = useI18n();
const { params } = useRoute();

/* Service injection */
const { push } = useRouter();
const { addErrorMessage, addSuccessMessage } = useMessagesStore();
const { course, getCourseByID } = useCourses();
const { project, createProject } = useProject();
const { setStructureChecks } = useStructureCheck();
const { setExtraChecks } = useExtraCheck();
const { dockerImages, getDockerImages, createDockerImage, deleteDockerImage } = useDockerImages();

/* State */
const loading = ref(true);

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
                addSuccessMessage(
                    t('toasts.messages.success'),
                    t('toasts.messages.projects.create.success', [project.value?.name]),
                );
                await push({
                    name: 'course-project',
                    params: { courseId: course.value.id, projectId: project.value.id },
                });
            } else {
                addErrorMessage(t('views.projects.create.error'), t('views.projects.create.error_description'));
            }
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

/* Load course data */
watchImmediate(
    () => params.courseId.toString(),
    async (courseId: string) => {
        loading.value = true;
        try {
            await getCourseByID(courseId);
            await getDockerImages();
        } catch (error: any) {
            processError(error);
        }
        loading.value = false;
    },
);
</script>

<template>
    <BaseLayout>
        <!-- Create project heading -->
        <Title class="mb-6">
            {{ t('views.projects.create') }}
        </Title>
        <template v-if="!loading">
            <div class="fadein">
                <!-- Project form -->
                <template v-if="dockerImages !== null && course !== null">
                    <ProjectForm
                        :course="course"
                        :docker-images="dockerImages"
                        @update:project="(project, numberOfGroups) => saveProject(project, numberOfGroups)"
                        @create:docker-image="saveDockerImage"
                        @delete:docker-image="removeDockerImage"
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

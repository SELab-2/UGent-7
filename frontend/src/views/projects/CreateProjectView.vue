<script setup lang="ts">
import BaseLayout from '@/components/layout/base/BaseLayout.vue';
import Title from '@/components/layout/Title.vue';
import { onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useCourses } from '@/composables/services/course.service';
import ProjectForm from '@/components/projects/ProjectForm.vue';
import { Project } from '@/types/Project.ts';
import { useProject } from '@/composables/services/project.service.ts';
import { processError } from '@/composables/services/helpers.ts';
import { useStructureCheck } from '@/composables/services/structure_check.service.ts';

/* Composable injections */
const { t } = useI18n();
const { params } = useRoute();

/* Service injection */
const { push } = useRouter();
const { course, getCourseByID } = useCourses();
const { project, createProject } = useProject();
const { setStructureChecks } = useStructureCheck();

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
                await setStructureChecks(newProject.structure_checks, project.value.id);
                await push({ name: 'course-project', params: { courseId: course.value.id, projectId: project.value.id } });
            }
        }
    } catch (error: any) {
        processError(error);
    }
}

/* Load course data */
onMounted(async () => {
    await getCourseByID(params.courseId as string);
});
</script>

<template>
    <BaseLayout>
        <!-- Create project heading -->
        <Title class="mb-6">
            {{ t('views.projects.create') }}
        </Title>

        <!-- Project form -->
        <ProjectForm :course="course" v-if="course !== null" @update:project="(project, numberOfGroups) => saveProject(project, numberOfGroups)" />
    </BaseLayout>
</template>

<style scoped></style>

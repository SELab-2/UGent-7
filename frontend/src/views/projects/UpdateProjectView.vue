<script setup lang="ts">
import BaseLayout from '@/components/layout/base/BaseLayout.vue';
import Title from '@/components/layout/Title.vue';
import ProjectForm from '@/components/projects/ProjectForm.vue';
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useProject } from '@/composables/services/project.service';

/* Composable injections */
const { t } = useI18n();
const { params } = useRoute();

/* Service injection */
const { project, getProjectByID } = useProject();

/* Load project data */
onMounted(async () => {
    await getProjectByID(params.projectId as string);
});

</script>

<template>
    <BaseLayout>
        <!-- Update project heading -->
        <Title class="mb-6">
            {{ t('views.projects.edit') }}
        </Title>

        <!-- Project form -->
        <ProjectForm :course="project.course" :project="project" v-if="project !== null"/>
    </BaseLayout>
</template>

<style scoped></style>
@/types/Project

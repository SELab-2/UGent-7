<script setup lang="ts">
import BaseLayout from '@/components/layout/base/BaseLayout.vue';
import ProjectList from '@/components/projects/ProjectList.vue';
import Title from '@/components/layout/Title.vue';
import { watch } from 'vue';
import { storeToRefs } from 'pinia';
import { useAuthStore } from '@/store/authentication.store.ts';
import { useI18n } from 'vue-i18n';
import { useProject } from '@/composables/services/project.service.ts';

/* Composable injections */
const { t } = useI18n();
const { user } = storeToRefs(useAuthStore());
const { projects, getProjectsByStudent, getProjectsByTeacher, getProjectsByAssistant } = useProject();

watch(
    user,
    async () => {
        if (user.value !== null) {
            projects.value = null;

            if (user.value.isStudent()) {
                await getProjectsByStudent(user.value.id);
            }

            if (user.value.isTeacher()) {
                await getProjectsByTeacher(user.value.id);
            }

            if (user.value.isAssistant()) {
                await getProjectsByAssistant(user.value.id);
            }
        }
    },
    { immediate: true },
);
</script>

<template>
    <BaseLayout>
        <!-- Project list title -->
        <Title class="mb-6">{{ t('views.dashboard.projects') }}</Title>
        <ProjectList :projects="projects" />
    </BaseLayout>
</template>

<style scoped lang="scss"></style>

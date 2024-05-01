<script setup lang="ts">
import { type Project } from '@/types/Project.ts';
import { useI18n } from 'vue-i18n';

/* Props */
defineProps<{
    project: Project;
}>();

/* Composable injections */
const { t } = useI18n();
</script>

<template>
    <div class="flex align-items-center flex-wrap gap-3 surface-50 p-3">
        <span class="flex align-items-center">
            <template v-if="project.isLocked()">
                <i class="pi pi-lock mr-2"/>
                {{ t('views.projects.locked') }}
            </template>
            <template v-else>
                <i class="pi pi-unlock mr-2"/>
                {{ t('views.projects.unlocked') }}
            </template>
        </span>
        <span class="flex align-items-center">
            <i class="pi pi-play mr-2" />
            {{ project.getFormattedStartDate() }}
        </span>
        <span class="flex align-items-center">
            <i class="pi pi-clock mr-2" />
            {{ project.getFormattedDeadline() }}
            ({{
                t(
                    'views.projects.days',
                    { hour: project.getFormattedDeadlineHour() },
                    project.getDaysLeft(),
                ).toLowerCase()
            }})
        </span>
        <span class="flex align-items-center">
            <i class="pi pi-users mr-2" />
            {{ t('views.projects.groupSize', project.group_size) }}
        </span>
    </div>
</template>

<style scoped lang="scss"></style>

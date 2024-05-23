<script setup lang="ts">
import Card from 'primevue/card';
import ProjectMeter from '@/components/submissions/ProjectMeter.vue';
import Button from 'primevue/button';
import { type Project } from '@/types/Project.ts';
import { PrimeIcons } from 'primevue/api';
import { type Course } from '@/types/Course.ts';
import { useI18n } from 'vue-i18n';
import type { Group } from '@/types/Group.ts';

/* Props */
const props = defineProps<{
    project: Project;
    course: Course;
    studentGroups: Group[];
}>();

/* Composable injections */
const { t } = useI18n();

/**
 * Return True if the user is in a group in this project.
 *
 * @returns {boolean} True if the user is in a group in this project.
 */
function isInGroup(): boolean {
    return props.studentGroups.some((group) => group.project.id === props.project.id);
}
</script>

<template>
    <Card class="border-round project-card">
        <template #header>
            <h2 class="text-primary m-0 text-xl flex align-items-center gap-2">
                <span class="pi pi-book text-xl mr-2" /> {{ course.name }}
            </h2>
        </template>
        <template #subtitle>
            {{ project.name }}
        </template>
        <template #content>
            <div class="mb-2">
                <i :class="['pi', PrimeIcons.PLAY, 'icon-color']" class="mr-2"></i>
                <b>{{ t('views.projects.start') }}</b
                >: {{ project.getFormattedStartDate() }}<br />
            </div>
            <div class="mb-2">
                <i :class="['pi', PrimeIcons.CALENDAR_PLUS, 'icon-color']" class="mr-2"></i>
                <b>{{ t('views.projects.deadline') }}</b
                >: {{ project.getFormattedDeadline() }}<br />
            </div>
            <div>
                <ProjectMeter :project="project" />
            </div>
        </template>
        <template #footer>
            <div class="flex justify-content-between">
                <RouterLink
                    :to="{
                        name: 'course-project',
                        params: {
                            courseId: course.id,
                            projectId: project.id,
                        },
                    }"
                >
                    <Button
                        class="align-self-end"
                        :icon="PrimeIcons.ARROW_RIGHT"
                        :label="t('components.card.open')"
                        icon-pos="right"
                        outlined
                    />
                </RouterLink>
                <RouterLink
                    v-if="isInGroup()"
                    :to="{
                        name: 'submission',
                        params: {
                            courseId: course.id,
                            projectId: project.id,
                            groupId: '5',
                        },
                    }"
                >
                    <Button
                        class="align-self-end"
                        :icon="PrimeIcons.ARROW_RIGHT"
                        :label="t('components.card.submit')"
                        icon-pos="right"
                        outlined
                    />
                </RouterLink>
            </div>
        </template>
    </Card>
</template>

<style lang="scss">
.project-card {
    border-style: solid;
    border-width: 1px;
    border-color: var(--primary-color-light);
    display: flex;
    flex-direction: column;
    height: 100%;

    .p-card-body {
        background: white;
    }

    .p-card-header {
        padding: var(--content-padding);
        background: var(--primary-color-light);
    }

    .p-card-content {
        display: flex;
        flex-direction: column;
        justify-content: space-between;

        .p-progressbar .p-progressbar-value {
            background-color: var(--primary-color);

            .p-progressbar-label {
                color: var(--primary-color-text);
            }
        }
    }
}
</style>

<script setup lang="ts">
import Card from 'primevue/card';
import Button from 'primevue/button';
import { type Project } from '@/types/Project.ts';
import { type Group } from '@/types/Group.ts';
import { PrimeIcons } from 'primevue/api';
import { useI18n } from 'vue-i18n';
import { watch } from 'vue';
import { type Course } from '@/types/Course.ts';
import { useSubmissionStatus } from '@/composables/services/submission_status.service.ts';
import ProjectMeter from '@/components/projects/ProjectMeter.vue';

/* Component props */
const props = withDefaults(
    defineProps<{
        type?: 'small' | 'large';
        project: Project;
        course: Course;
        projectGroups: Group[];
        studentGroups: Group[];
    }>(),
    {
        type: 'large',
    },
);

/* Composable injections */
const { t } = useI18n();
const { submissionStatus, getSubmissionStatusByProject } = useSubmissionStatus();

/**
 * Return True if the user is in a group in this project.
 */
function isInGroup(): boolean {
    return props.studentGroups.some((group) => props.projectGroups.includes(group));
}

/* Watchers */
watch(
    props.course,
    () => {
        getSubmissionStatusByProject(props.project.id);
    },
    {
        immediate: true,
    },
);
</script>

<template>
    <template v-if="type === 'small'">
        <RouterLink
            class="text-color"
            :to="{
                name: 'course-project',
                params: {
                    courseId: course.id,
                    projectId: project.id,
                },
            }"
        >
            <div class="p-5 surface-300 border-round">
                <div class="flex align-items-center gap-5">
                    <i class="pi pi-clock text-6xl text-primary" />
                    <div class="w-full">
                        <h3 class="m-0">{{ project.name }}</h3>
                        <div class="flex justify-content-between align-items-center mt-2">
                            <span>{{ project.getFormattedDeadline() }}</span>
                            <span>{{
                                t(
                                    'views.projects.days',
                                    { hour: project.getFormattedDeadlineHour() },
                                    project.getDaysLeft(),
                                )
                            }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </RouterLink>
    </template>
    <template v-else>
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
                    <ProjectMeter :submission-status="submissionStatus" />
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

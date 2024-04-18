<script setup lang="ts">
import Card from 'primevue/card';
import Button from 'primevue/button';
import ProgressBar from 'primevue/progressbar';
import { type Project } from '@/types/Project.ts';
import { PrimeIcons } from 'primevue/api';
import { useI18n } from 'vue-i18n';
import { type Course } from '@/types/Course.ts';

/**
 * TODO
 *  - Submission check depends on more than just structure checks
 */

/* Component props */
withDefaults(
    defineProps<{
        type?: 'small' | 'large';
        project: Project;
        course: Course;
    }>(),
    {
        type: 'large',
    },
);

/* Composable injections */
const { t } = useI18n();
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
                    <i :class="['pi', PrimeIcons.INFO_CIRCLE, 'icon-color']" class="mr-2"></i>
                    <b>{{ t('views.projects.submissionStatus') }}</b
                    >: ok
                </div>
                <ProgressBar class="mt-3" :value="project.getProgress()">
                    {{ t('views.projects.days', { hour: project.getFormattedDeadlineHour() }, project.getDaysLeft()) }}
                </ProgressBar>
            </template>
            <template #footer>
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
µ

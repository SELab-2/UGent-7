<script setup lang="ts">
import moment from 'moment';
import MeterGroup from 'primevue/metergroup';
import Card from 'primevue/card';
import Button from 'primevue/button';
import ProgressBar from 'primevue/progressbar';
import { type Project } from '@/types/Project.ts';
import { PrimeIcons } from 'primevue/api';
import { useI18n } from 'vue-i18n';
import { computed, watch } from 'vue';
import { type Course } from '@/types/Course.ts';
import { useSubmissionStatus } from '@/composables/services/submission_status.service.ts';

/**
 * TODO
 *  - Submission check depends on more than just structure checks
 */

/* Component props */
const props = withDefaults(
    defineProps<{
        type?: 'small' | 'large';
        project: Project;
        course: Course;
    }>(),
    {
        type: 'large',
    },
);

const formattedDeadline = computed(() => {
    return moment(props.project.deadline).format('DD MMMM YYYY');
});

const formattedStartDate = computed(() => {
    return moment(props.project.start_date).format('DD MMMM YYYY');
});

const meterItems = computed(() => {
    const groups = submissionStatus.value?.non_empty_groups || 1;
    const groupsSubmitted = submissionStatus.value?.groups_submitted || 0;
    const submissionsPassed = submissionStatus.value?.submissions_passed || 0;
    const submissionsFailed = groupsSubmitted - submissionsPassed;
    return [
        { value: (submissionsPassed / groups) * 100, color: '#749b68', label: 'Succeeded tests', icon: 'pi pi-check' },
        { value: (submissionsFailed / groups) * 100, color: '#FF5445', label: 'Failed tests', icon: 'pi pi-times' },
    ]
})

/* Composable injections */
const { t } = useI18n();
const { submissionStatus, getSubmissionStatusByProject } = useSubmissionStatus();

/* Watchers */
watch(
    props.course,
    () => {

        getSubmissionStatusByProject(props.project.id)
    },
    {
        immediate: true,
    },
);

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
                <i :class="['pi', PrimeIcons.CALENDAR_PLUS, 'icon-color']" class="mr-2"></i>
                <b>{{ t('views.projects.deadline') }}</b
                >: {{ formattedDeadline }}<br />
            </div>
            <div>
                <i :class="['pi', PrimeIcons.INFO_CIRCLE, 'icon-color']" class="mr-2"></i>
                <b>{{ t('views.projects.submissionStatus') }}</b>:
                <MeterGroup v-if="(submissionStatus?.groups_submitted || 0) > 0" :value="meterItems" labelOrientation="vertical">
                    <template #start>
                        <div class="flex justify-between mt-2 relative">
                            <span>{{ submissionStatus?.groups_submitted }} {{ submissionStatus?.groups_submitted === 1 
                            ? t('components.card.submission') 
                            : t('components.card.submissions') }}</span>
                        <span class="w-full absolute text-right">{{ submissionStatus?.non_empty_groups }} Groups</span>
                        </div>
                    </template>
                </MeterGroup>
                <p v-else>
                    {{ t('components.card.noSubmissions') }}
                </p>
            </div>
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
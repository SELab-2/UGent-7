<script setup lang="ts">
import { computed } from 'vue';
import { type Submission } from '@/types/submission/Submission.ts';
import { type ExtraCheckResult } from '@/types/submission/ExtraCheckResult.ts';
import { type StructureCheckResult } from '@/types/submission/StructureCheckResult.ts';
import { useI18n } from 'vue-i18n';
import router from '@/router/router.ts';

const { t } = useI18n();

const props = defineProps<{
    submissions: Submission[];
}>();

/**
 * Returns the extra information for the submission
 */
const submissionsExtra = computed(() => {
    return props.submissions.map((submission: Submission) => {
        const iconDetails = getExtraSubmissionInformation(submission);
        return {
            ...submission,
            iconName: iconDetails.iconName,
            color: iconDetails.color,
            hoverText: iconDetails.hoverText,
        };
    });
});

/**
 * Returns the icon name, color and hover text for the submission
 * @param submission
 */
const getExtraSubmissionInformation = (
    submission: Submission,
): { iconName: string; color: string; hoverText: string } => {
    if (
        !(
            submission.extraCheckResults.map((check: ExtraCheckResult) => check.result === 'SUCCESS').every(Boolean) ||
            submission.structureCheckResults
                .map((check: StructureCheckResult) => check.result === 'SUCCESS')
                .every(Boolean)
        )
    ) {
        return { iconName: 'times', color: 'red', hoverText: t('views.submissions.hoverText.allChecksFailed') };
    } else if (
        !submission.extraCheckResults.map((check: ExtraCheckResult) => check.result === 'SUCCESS').every(Boolean)
    ) {
        return { iconName: 'cloud', color: 'lightblue', hoverText: t('views.submissions.hoverText.extraChecksFailed') };
    } else if (
        !submission.structureCheckResults
            .map((check: StructureCheckResult) => check.result === 'SUCCESS')
            .every(Boolean)
    ) {
        return { iconName: 'bolt', color: 'yellow', hoverText: t('views.submissions.hoverText.structureChecksFailed') };
    } else {
        return { iconName: 'check', color: 'lightgreen', hoverText: t('views.submissions.hoverText.allChecksPassed') };
    }
};

/**
 * Returns the time parsed since the submission
 * @param submissionDate
 */
const timeSince = (submissionDate: Date): string => {
    const today = new Date();
    const diffTime = new Date(today.getTime() - submissionDate.getTime());
    const diffDays = Math.floor(diffTime.getTime() / (1000 * 60 * 60 * 24));

    if (diffDays === 0) {
        return t('views.submissions.timeSince.today');
    } else if (diffDays <= 7) {
        return `${diffDays} ${t('views.submissions.timeSince.daysAgo')}`;
    } else if (diffDays <= 30) {
        return t('views.submissions.timeSince.weekAgo');
    } else {
        return t('views.submissions.timeSince.monthAgo');
    }
};

/**
 * Navigates to the submission with the given id
 * @param submissionId
 */
const navigateToSubmission = (submissionId: string): void => {
    router.push({ name: 'submission', params: { submissionId, groupId: '0', projectId: '0', courseId: '0' } });
};
</script>

<template>
    <div>
        <div
            v-for="submission in submissionsExtra?.reverse()"
            :key="submission.id"
            class="flex submission align-content-center align-items-center"
            v-tooltip="submission.hoverText"
            @click="navigateToSubmission(submission.id)"
        >
            <p
                :class="'font-semibold m-2 p-1 pi pi-' + submission.iconName"
                :style="{ color: submission.color, fontSize: '1.25rem' }"
            ></p>
            <label class="font-semibold m-2 p-1">#{{ submission.submission_number }} </label>
            <p>{{ timeSince(submission.submission_time) }}</p>
        </div>
    </div>
</template>

<style scoped lang="scss">
@import '@/assets/scss/theme/theme.scss';
.submission {
    border-bottom: 1.5px solid var(--primary-color);
    cursor: pointer;
}
.submission:last-child {
    border-bottom: none;
}
</style>

<script setup lang="ts">
import { type Submission } from '@/types/submission/Submission.ts';
import { useI18n } from 'vue-i18n';
import router from '@/router/router.ts';
import { useRoute } from 'vue-router';
import { PrimeIcons } from 'primevue/api';
import { type Group } from '@/types/Group.ts';
import { computed } from 'vue';

const { params } = useRoute();
const { t } = useI18n();

const props = defineProps<{
    submissions: Submission[];
    group: Group | null;
}>();

/* The sorted submissions */
const sortedSubmissions = computed(() => [...props.submissions].sort((a, b) => parseInt(b.id) - parseInt(a.id)));

/**
 * Returns the description for the submission
 * @param submission
 */
function getSubmissionDescription(submission: Submission): string {
    if (submission.isPassed()) {
        return t('views.submissions.hoverText.allChecksPassed');
    } else if (!submission.isStructureCheckPassed()) {
        return t('views.submissions.hoverText.structureChecksFailed');
    } else if (!submission.isExtraCheckPassed()) {
        return t('views.submissions.hoverText.extraChecksFailed');
    }

    return t('views.submissions.hoverText.allChecksFailed');
}

/**
 * Returns the icon for the submission.
 *
 * @param submission
 */
function getSubmissionIcon(submission: Submission): string {
    if (submission.isPassed()) {
        return PrimeIcons.CHECK;
    } else if (!submission.isStructureCheckPassed()) {
        return PrimeIcons.SITEMAP;
    } else if (!submission.isExtraCheckPassed()) {
        return PrimeIcons.BOLT;
    }

    return PrimeIcons.TIMES;
}

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
    const tmpGroupId = props.group?.id ?? params.groupId;
    void router.push({
        name: 'submission',
        params: { submissionId, groupId: tmpGroupId, projectId: params.projectId, courseId: params.courseId },
    });
};
</script>

<template>
    <template v-if="sortedSubmissions.length > 0">
        <div
            v-for="submission in sortedSubmissions"
            :key="submission.id"
            class="px-3 py-2 surface-100 gap-2 mb-3 flex submission justify-content-between align-items-center"
            @click="navigateToSubmission(submission.id)"
        >
            <div class="flex align-items-center gap-2">
                <label class="font-semibold m-2 p-1">#{{ submission.submission_number }}</label>
                <div
                    class="status border-circle p-2 w-2rem h-2rem flex align-items-center justify-content-center"
                    :class="{
                        ['passed']: submission.isPassed(),
                        ['failed-extra']: !submission.isExtraCheckPassed(),
                        ['failed-structure']: !submission.isStructureCheckPassed(),
                    }"
                >
                    <i :class="getSubmissionIcon(submission)" class="text-lg text-xs"></i>
                </div>
                <p>{{ timeSince(submission.submission_time) }}</p>
            </div>
            <p>{{ getSubmissionDescription(submission) }}</p>
        </div>
    </template>
    <template v-else>
        {{ t('views.submissions.noSubmissions') }}
    </template>
</template>

<style scoped lang="scss">
.submission {
    transition: all 0.3s ease;
    cursor: pointer;

    &:hover {
        background-color: var(--surface-300) !important;
    }

    .status {
        &.passed {
            background-color: var(--bg-primary);
            color: var(--primary-color-text);
        }

        &.failed-structure {
            background-color: indianred;
            color: white;
        }

        &.failed-extra:not(.failed-structure) {
            background-color: var(--secondary-color);
        }
    }
}
</style>

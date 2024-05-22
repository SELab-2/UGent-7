<script setup lang="ts">
import Title from '@/components/layout/Title.vue';
import BaseLayout from '@/components/layout/base/BaseLayout.vue';
import Textarea from 'primevue/textarea';
import { storeToRefs } from 'pinia';
import { useAuthStore } from '@/store/authentication.store.ts';
import Button from 'primevue/button';
import { useI18n } from 'vue-i18n';
import { computed, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useFeedback } from '@/composables/services/feedback.service.ts';
import { type Feedback } from '@/types/Feedback.ts';
import { User } from '@/types/users/User.ts';
import moment from 'moment/moment';
import { PrimeIcons } from 'primevue/api';
import { useSubmission } from '@/composables/services/submission.service.ts';
import { useProject } from '@/composables/services/project.service.ts';

/* Composable injections */
const route = useRoute();
const { t } = useI18n();
const { user } = storeToRefs(useAuthStore());
const { submission, getSubmissionByID } = useSubmission();
const { feedbacks, getFeedbackBySubmission, createFeedback, updateFeedback } = useFeedback();
const { project, getProjectByID } = useProject();

/* Feedback content */
const feedbackTextValue = ref<string>('');
const editedFeedback = ref<Feedback | null>(null);

function editFeedback(feedback: Feedback): void {
    feedbackTextValue.value = feedback.message;
    editedFeedback.value = feedback;
}

/**
 * Submit feedback depending if the feedback is being edited or created
 */
function submitFeedback(): void {
    if (editedFeedback.value === null) {
        createFeedback(feedbackTextValue.value, route.params.submissionId as string);
        feedbackTextValue.value = '';
    } else {
        updateFeedback(feedbackTextValue.value, editedFeedback.value.id);
        feedbackTextValue.value = '';
        editedFeedback.value = null;
    }
    getFeedbackBySubmission(route.params.submissionId as string);
}

/* Computed Properties */
const structureAndExtraFaults = computed(() => {
    if (submission.value == null) return [];

    const structureFaults = submission.value.structureCheckFaults();
    const extraFaults = submission.value.isStructureCheckPassed() ? submission.value.extraCheckFaults() : [];

    return [...structureFaults, ...extraFaults];
});

const showLogsAndArtifacts = computed(() => {
    const extraChecks = submission.value?.extraCheckResults ?? [];
    let results: string[] = [];

    if (project.value != null) {
        const visibleLogs = extraChecks
            .filter((check) => {
                return project.value?.extra_checks?.find((extraCheck) => extraCheck.id === check.id)?.show_log;
            })
            .map((check) => check.log_file);

        const visibleArtifacts = extraChecks
            .filter((check) => {
                return project.value?.extra_checks?.find((extraCheck) => extraCheck.id === check.id)?.show_log;
            })
            .map((check) => check.artifact);

        results = [...visibleLogs, ...visibleArtifacts];
    }

    return results;
});

/* Watchers */
// A watch to update the feedbacks when a new feedback is added
watch(
    feedbacks,
    (newFeedbacks) => {
        feedbacks.value = newFeedbacks;
    },
    { deep: true, immediate: true },
);

// A watch on submissionId url parameter to get the feedbacks
watch(
    () => route.params.submissionId,
    (submissionId) => {
        getSubmissionByID(submissionId as string);
        getFeedbackBySubmission(submissionId as string);
        getProjectByID(route.params.projectId as string);
    },
    { immediate: true },
);
</script>

<template>
    <BaseLayout>
        <div class="grid">
            <!-- Submission properties -->
            <div v-if="submission" class="col-6 md:col-4">
                <!-- Submission status -->
                <div>
                    <Title class="flex">Status</Title>
                    <div class="p-2">
                        <p v-if="submission.isPassed()">{{ t('views.submissions.passed') }}</p>
                        <div v-else>
                            <span>{{ t('views.submissions.failed') }}</span>
                            <ul class="m-1">
                                <li v-for="fault in structureAndExtraFaults" :key="fault">{{ t(fault) }}</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <!-- Submission Downloadable zip -->
                <div>
                    <Title v-if="showLogsAndArtifacts.length > 0" class="flex">{{ t('views.submissions.file') }}</Title>
                    <Title v-else class="flex"> {{ t('views.submissions.files') }} </Title>
                    <div>
                        <ul>
                            <li v-if="submission.zip">
                                <a :href="submission.zip" download>
                                    {{ t('views.submissions.downloadZip') }}
                                </a>
                            </li>
                            <li v-else>
                                {{ t('views.submissions.no_zip_available') }}
                            </li>
                            <li v-for="(item, index) in showLogsAndArtifacts" :key="index">
                                <a :href="item" download> {{ t('views.submissions.downloadLog', [index + 1]) }} </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <!-- Feedback section -->
            <div class="col-8 md:col-7">
                <!-- Written Feedback overview -->
                <div class="feedback-section mb-3">
                    <Title class="flex mb-3">Feedback</Title>
                    <!-- Single Feedback component -->
                    <div v-if="feedbacks !== null && feedbacks.length > 0">
                        <div v-for="feedback in feedbacks" :key="feedback.id">
                            <div class="feedback-header-wrap">
                                <!-- Single feedback header -->
                                <p class="feedback-header mt-1">
                                    {{
                                        t('views.submissions.feedback.dateAndAuthor', [
                                            moment(feedback.creation_date).format('DD MMMM YYYY'),
                                            User.fromJSON(feedback.author).getFullName(),
                                        ])
                                    }}
                                </p>
                                <!-- Edit feedback button -->
                                <Button
                                    v-tooltip.top="t('views.submissions.feedback.edit')"
                                    v-if="user?.isTeacher() && feedback.author.id === user?.id"
                                    :icon="PrimeIcons.PENCIL"
                                    icon-pos="right"
                                    style="height: 35px; width: 35px"
                                    @click="editFeedback(feedback)"
                                />
                            </div>
                            <p class="feedback-message">{{ feedback.message }}</p>
                        </div>
                    </div>
                    <p v-else class="pt-2 pl-2">{{ t('views.submissions.feedback.noFeedback') }}</p>
                </div>
                <!-- Write feedback -->
                <div v-if="user?.isTeacher()">
                    <form @submit.prevent="submitFeedback">
                        <Textarea
                            id="feedback"
                            v-model="feedbackTextValue"
                            class="w-full"
                            :placeholder="t('views.submissions.feedback.writeFeedback')"
                        />
                        <Button
                            class="mt-2"
                            :label="t('views.submissions.feedback.addFeedback')"
                            type="submit"
                            iconPos="right"
                        />
                    </form>
                </div>
            </div>
        </div>
    </BaseLayout>
</template>

<style scoped lang="scss">
.p-inputtextarea {
    width: 100%;
    height: 8rem;
}
.feedback-section {
    border-bottom: 4px solid var(--primary-color);
}
.feedback-header {
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    margin-bottom: 0.25rem;
}
.feedback-header-wrap {
    border-bottom: 1px solid lightgray;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.feedback-message {
    word-wrap: break-word;
    overflow-wrap: break-word;
    width: 100%;
}
</style>

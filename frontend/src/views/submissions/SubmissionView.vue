<script setup lang="ts">
import Title from '@/views/layout/Title.vue';
import BaseLayout from '@/views/layout/base/BaseLayout.vue';
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
import { useExtraCheck } from '@/composables/services/extra_checks.service.ts';

/* Composable injections */
const route = useRoute();
const { t } = useI18n();
const { user } = storeToRefs(useAuthStore());
const { submission, getSubmissionByID } = useSubmission();
const { feedbacks, getFeedbackBySubmission, createFeedback, updateFeedback } = useFeedback();
const { project, getProjectByID } = useProject();
const { extraChecks, getExtraChecksByProject } = useExtraCheck();

/* Feedback content */
const feedbackTextValue = ref<string>('');
const editedFeedback = ref<Feedback | null>(null);

function editFeedback(feedback: Feedback): void {
    feedbackTextValue.value = feedback.message;
    editedFeedback.value = feedback;
}

/**
 * Submit feedback depending on if the feedback is being edited or created
 */
async function submitFeedback(): Promise<void> {
    try {
        if (editedFeedback.value === null) {
            await createFeedback(feedbackTextValue.value, route.params.submissionId as string);
            feedbackTextValue.value = '';
        } else {
            await updateFeedback(feedbackTextValue.value, editedFeedback.value.id);
            feedbackTextValue.value = '';
            editedFeedback.value = null;
        }
        await getFeedbackBySubmission(route.params.submissionId as string);
    } catch (e) {
        console.error(e);
    }
}

/* Computed Properties */
const structureAndExtraFaults = computed(() => {
    if (submission.value == null) return [];

    const structureFaults = submission.value.structureCheckFaults();
    const extraFaults = submission.value.isStructureCheckPassed() ? submission.value.extraCheckFaults() : [];

    // Filter out empty faults
    return [...structureFaults, ...extraFaults].filter((fault) => fault);
});

const showLogsAndArtifacts = computed(() => {
    const extraChecksResults = submission.value?.extraCheckResults ?? [];
    let results: string[] = [];
    if (project.value != null && extraChecks.value != null) {
        const visibleLogs = extraChecksResults
            .filter((check) => {
                return extraChecks.value?.find((extraCheck) => extraCheck.id === check.extra_check)?.show_log;
            })
            .map((check) => check.log_file);

        const visibleArtifacts = extraChecksResults
            .filter((check) => {
                return extraChecks.value?.find((extraCheck) => extraCheck.id === check.extra_check)?.show_artifact;
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
        getExtraChecksByProject(route.params.projectId as string);
    },
    { immediate: true },
);
</script>

<template>
    <BaseLayout>
        <RouterLink :to="{ name: 'submissions' }">
            <Button
                class="mb-4 p-0 text-sm text-black-alpha-70"
                :icon="PrimeIcons.ARROW_LEFT"
                :label="t('views.submissions.backToSubmissions')"
                link
            />
        </RouterLink>
        <div class="grid">
            <!-- Submission properties -->
            <div v-if="submission" class="col-6 md:col-4">
                <!-- Submission status -->
                <div>
                    <Title class="flex">Status</Title>
                    <div class="pl-2 mt-4">
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
            <div class="col-12 md:col-7">
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
                    <p v-else class="pt-2">{{ t('views.submissions.feedback.noFeedback') }}</p>
                </div>
                <!-- Write feedback -->
                <div v-if="user?.isTeacher()">
                    <form @submit.prevent="submitFeedback">
                        <Textarea
                            id="feedback"
                            v-model="feedbackTextValue"
                            class="w-full h-10rem"
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

<style scoped lang="scss"></style>

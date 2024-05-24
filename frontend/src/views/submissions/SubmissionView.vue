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
import moment from 'moment/moment';
import { PrimeIcons } from 'primevue/api';
import { useSubmission } from '@/composables/services/submission.service.ts';
import DownloadCard from '@/components/submissions/DownloadCard.vue';
import { watchImmediate } from '@vueuse/core';
import Loading from '@/components/Loading.vue';

/* Composable injections */
const route = useRoute();
const { t } = useI18n();
const { user } = storeToRefs(useAuthStore());
const { submission, getSubmissionByID } = useSubmission();
const { feedbacks, getFeedbackBySubmission, createFeedback, updateFeedback } = useFeedback();

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

const artifacts = computed<string[] | null>(() => {
    if (submission.value != null) {
        return submission.value.extraCheckResults
            .filter((extraCheck) => extraCheck.artifact)
            .map((extraCheck) => extraCheck.artifact);
    }

    return null;
});

const logs = computed<string[] | null>(() => {
    if (submission.value != null) {
        return submission.value.extraCheckResults
            .filter((extraCheck) => extraCheck.log_file)
            .map((extraCheck) => extraCheck.log_file);
    }

    return null;
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
watchImmediate(
    () => route.params.submissionId,
    (submissionId) => {
        getSubmissionByID(submissionId.toString());
        getFeedbackBySubmission(submissionId.toString());
    },
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
        <template v-if="submission !== null">
            <div class="fadein grid">
                <!-- Submission properties -->
                <div class="col-6 md:col-4">
                    <!-- Submission status -->
                    <div class="mb-5">
                        <Title class="flex">Status</Title>
                        <div class="mt-4">
                            <p v-if="submission.isPassed()">{{ t('views.submissions.passed') }}</p>
                            <div v-else>
                                <span>{{ t('views.submissions.failed') }}</span>
                                <ul>
                                    <li v-for="fault in structureAndExtraFaults" :key="fault">
                                        {{ t(fault) }}
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <!-- Submission Downloadable zip -->
                    <template v-if="logs !== null && artifacts !== null">
                        <Title v-if="logs.length > 0 || artifacts.length > 0" class="flex">{{
                            t('views.submissions.file')
                        }}</Title>
                        <Title v-else class="flex"> {{ t('views.submissions.files') }} </Title>
                        <div class="flex flex-column gap-3">
                            <DownloadCard :title="t('views.submissions.downloadZip')" :href="submission.zip" />
                            <DownloadCard
                                :title="t('views.submissions.downloadLog', [index + 1])"
                                :href="log"
                                :key="index"
                                v-for="(log, index) in logs"
                            />
                            <DownloadCard
                                :title="t('views.submissions.downloadArtifact', [index + 1])"
                                :href="artifact"
                                :key="index"
                                v-for="(artifact, index) in artifacts"
                            />
                        </div>
                    </template>
                    <template v-else>
                        <Loading />
                    </template>
                </div>
                <!-- Feedback section -->
                <div class="col-12 md:col-7">
                    <!-- Written Feedback overview -->
                    <div class="feedback-section mb-3">
                        <Title class="flex mb-3">Feedback</Title>
                        <!-- Single Feedback component -->
                        <template v-if="feedbacks !== null">
                            <template v-if="feedbacks.length > 0">
                                <div v-for="feedback in feedbacks" :key="feedback.id">
                                    <div class="flex justify-content-between">
                                        <!-- Single feedback header -->
                                        <p class="mt-1">
                                            {{
                                                t('views.submissions.feedback.dateAndAuthor', [
                                                    moment(feedback.creation_date).format('DD MMMM YYYY'),
                                                    feedback.author.getFullName(),
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
                                    <p class="mb-5 surface-100 p-3">
                                        {{ feedback.message }}
                                    </p>
                                </div>
                            </template>
                            <template v-else>{{ t('views.submissions.feedback.noFeedback') }}</template>
                        </template>
                        <template v-else>
                            <Loading />
                        </template>
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
        </template>
        <template v-else>
            <Loading height="60vh" />
        </template>
    </BaseLayout>
</template>

<style scoped lang="scss"></style>

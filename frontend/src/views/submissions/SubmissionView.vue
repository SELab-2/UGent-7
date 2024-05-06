<script setup lang="ts">
import Title from '@/components/layout/Title.vue';
import BaseLayout from '@/components/layout/base/BaseLayout.vue';
import Textarea from 'primevue/textarea';
import { storeToRefs } from 'pinia';
import { useAuthStore } from '@/store/authentication.store.ts';
import Button from 'primevue/button';
import { useI18n } from 'vue-i18n';
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useFeedback } from '@/composables/services/feedback.service.ts';
import { type Feedback } from '@/types/Feedback.ts';
import { User } from '@/types/users/User.ts';
import moment from 'moment/moment';
import { PrimeIcons } from 'primevue/api';
import {useSubmission} from "@/composables/services/submission.service.ts";

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
    },
    { immediate: true },
);
</script>

<template>
    <BaseLayout>
        <div class="grid">
            <!-- Submission properties -->
            <div class="col-6 md:col-4">
                <!-- Submission status -->
                <div>
                    <Title class="flex">Status</Title>
                </div>
                <!-- Submission Downloadable zip -->
                <div>
                    <Title class="flex">File(s)</Title>
                    <!-- TODO change this to zip -->
                    {{ submission! }}
                    <div v-if="submission">
                        <a :href="submission.files[0].webkitRelativePath" download class="download-link">
                            Download Submission
                        </a>
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

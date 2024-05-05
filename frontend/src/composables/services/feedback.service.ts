import { Feedback } from '@/types/Feedback.ts';
import { ref, type Ref, type UnwrapRef } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { create, patch, getList } from '@/composables/services/helpers.ts';
import type { Response } from '@/types/Response.ts';

interface FeedbackState {
    feedback: Ref<Feedback | null>;
    feedbacks: Ref<Feedback[] | null>;
    getFeedbackBySubmission: (submissionId: string) => Promise<void>;
    createFeedback: (feedbackMessage: UnwrapRef<string>, submissionId: string) => Promise<void>;
    updateFeedback: (feedbackMessage: UnwrapRef<string>, feedbackId: string) => Promise<void>;
}

export function useFeedback(): FeedbackState {
    const feedback = ref<Feedback | null>(null);
    const feedbacks = ref<Feedback[] | null>(null);
    const response = ref<Response | null>(null);

    async function getFeedbackBySubmission(submissionId: string): Promise<void> {
        const endpoint = endpoints.feedbacks.bySubmission.replace('{submissionId}', submissionId);
        await getList<Feedback>(endpoint, feedbacks, Feedback.fromJSON);
    }

    async function createFeedback(feedbackMessage: string, submissionId: string): Promise<void> {
        const endpoint = endpoints.feedbacks.bySubmission.replace('{submissionId}', submissionId);
        await create<Feedback>(
            endpoint,
            {
                message: feedbackMessage,
            },
            feedback,
            Feedback.fromJSON,
            'multipart/form-data',
        );
    }

    async function updateFeedback(updatedMessage: string, feedbackId: string): Promise<void> {
        const endpoint = endpoints.feedbacks.retrieve.replace('{id}', feedbackId);
        await patch(
            endpoint,
            {
                message: updatedMessage,
            },
            response,
            'multipart/form-data',
        );
    }

    return {
        feedback,
        feedbacks,
        getFeedbackBySubmission,
        createFeedback,
        updateFeedback,
    };
}

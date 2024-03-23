import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get} from '@/composables/services/helpers.ts';
import { SubmissionStatus } from '@/types/SubmisionStatus';

export function useSubmission() {
    const submissionStatus = ref<SubmissionStatus|null>(null);

    async function getSubmissionStatus(project_id: number) {
        const endpoint = endpoints.submissions.status.replace('{project_id}', project_id.toString());
        get<SubmissionStatus>(endpoint, submissionStatus, SubmissionStatus.fromJSON);
        console.log(submissionStatus)
    }

    return {
        submissionStatus,
        getSubmissionStatus
    };
}
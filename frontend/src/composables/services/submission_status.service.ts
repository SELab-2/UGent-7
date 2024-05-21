import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get } from '@/composables/services/helpers.ts';
import { SubmissionStatus } from '@/types/SubmisionStatus';

interface SubmissionStatusState {
    submissionStatus: Ref<SubmissionStatus | null>;
    getSubmissionStatusByProject: (projectId: string) => Promise<void>;
}

export function useSubmissionStatus(): SubmissionStatusState {
    const submissionStatus = ref<SubmissionStatus | null>(null);

    async function getSubmissionStatusByProject(projectId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.submissions.status.replace('{projectId}', projectId);
        await get<SubmissionStatus>(endpoint, submissionStatus, SubmissionStatus.fromJSON, selfprocessError);
    }

    return {
        submissionStatus,
        getSubmissionStatusByProject,
    };
}

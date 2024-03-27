import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get} from '@/composables/services/helpers.ts';
import { SubmissionStatus } from '@/types/SubmisionStatus';
import {ComposerTranslation} from "vue-i18n";

export function useSubmission() {
    const submissionStatus = ref<SubmissionStatus|null>(null);
    
    async function getSubmissionStatus(project_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.submissions.status.replace('{project_id}', project_id);
        await get<SubmissionStatus>(endpoint, submissionStatus, SubmissionStatus.fromJSON, t);
    }

    return {
        submissionStatus,
        getSubmissionStatus
    };
}
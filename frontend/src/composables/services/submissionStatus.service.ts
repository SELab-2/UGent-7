import { ref } from 'vue'
import { endpoints } from '@/config/endpoints.ts'
import { get } from '@/composables/services/helpers.ts'
import { SubmissionStatus } from '@/types/SubmisionStatus'

export function useSubmissionStatus() {
    const submissionStatus = ref<SubmissionStatus | null>(null)

    async function getSubmissionStatusByProject(projectId: string) {
        const endpoint = endpoints.submissions.status.replace(
            '{projectId}',
            projectId
        )
        await get<SubmissionStatus>(
            endpoint,
            submissionStatus,
            SubmissionStatus.fromJSON
        )
    }

    return {
        submissionStatus,
        getSubmissionStatusByProject
    }
}

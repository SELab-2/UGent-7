import { ref } from 'vue'
import { endpoints } from '@/config/endpoints.ts'
import { get } from '@/composables/services/helpers.ts'
import { SubmissionStatus } from '@/types/SubmisionStatus'

export function useSubmission_status() {
    const submissionStatus = ref<SubmissionStatus | null>(null)

    async function getSubmissionStatusByProject(project_id: string) {
        const endpoint = endpoints.submissions.status.replace(
            '{project_id}',
            project_id
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

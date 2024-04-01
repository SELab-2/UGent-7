import { describe, it, expect, beforeEach } from 'vitest'
import { useSubmission_status } from '@/composables/services/submissionStatus.service.ts'

const { submissionStatus, getSubmissionStatusByProject } =
    useSubmission_status()

describe('submision_status', (): void => {
    it('gets submision status data by project', async () => {
        await getSubmissionStatusByProject('0')
        expect(submissionStatus.value).not.toBeNull()
        expect(submissionStatus.value?.groups_submitted).toBe(1)
        expect(submissionStatus.value?.non_empty_groups).toBe(2)
        expect(submissionStatus.value?.submissions_passed).toBe(1)
    })
})

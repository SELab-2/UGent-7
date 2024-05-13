/* eslint-disable @typescript-eslint/no-unused-vars */
import { describe, it, expect } from 'vitest';
import { useSubmissionStatus } from '@/composables/services/submission_status.service.ts';

const { submissionStatus, getSubmissionStatusByProject } = useSubmissionStatus();

function resetService(): void {
    submissionStatus.value = null;
}

describe('submision_status', (): void => {
    it('gets submision status data by project', async () => {
        resetService();

        await getSubmissionStatusByProject('0');
        expect(submissionStatus.value).not.toBeNull();
        expect(submissionStatus.value?.groups_submitted).toBe(1);
        expect(submissionStatus.value?.non_empty_groups).toBe(2);
        // No need to check for structure_check_passed and extra_checks_passed since those queries are not implemented in the frontend
    });
});

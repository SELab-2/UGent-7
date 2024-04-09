/* eslint-disable @typescript-eslint/no-unused-vars */
import { describe, it, expect } from 'vitest';
import { useSubmissionStatus } from '@/composables/services/submission_status.service.ts';

const { submissionStatus, getSubmissionStatusByProject } = useSubmissionStatus();

describe('submision_status', (): void => {
    it('gets submision status data by project', async () => {
        await getSubmissionStatusByProject('0');
        expect(submissionStatus.value).not.toBeNull();
        expect(submissionStatus.value?.groups_submitted).toBe(1);
        expect(submissionStatus.value?.non_empty_groups).toBe(2);
        expect(submissionStatus.value?.submissions_passed).toBe(1);
    });
});

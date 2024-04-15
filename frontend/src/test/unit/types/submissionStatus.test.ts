import { describe, it, expect } from 'vitest';

import { SubmissionStatus } from '@/types/SubmisionStatus';
import { submissionStatusData } from './data';
import { createSubmissionStatus } from './helper';

describe('submissionStatus type', () => {
    it('create instance of submissionStatus with correct properties', () => {
        const submissionStatus = createSubmissionStatus(submissionStatusData);

        expect(submissionStatus).toBeInstanceOf(SubmissionStatus);
        expect(submissionStatus.non_empty_groups).toBe(submissionStatusData.non_empty_groups);
        expect(submissionStatus.groups_submitted).toBe(submissionStatusData.groups_submitted);
        expect(submissionStatus.submissions_passed).toBe(submissionStatusData.submissions_passed);
    });

    it('create a submissionStatus instance from JSON data', () => {
        const submissionStatusJSON = { ...submissionStatusData };
        const submissionStatus = SubmissionStatus.fromJSON(submissionStatusJSON);

        expect(submissionStatus).toBeInstanceOf(SubmissionStatus);
        expect(submissionStatus.non_empty_groups).toBe(submissionStatusData.non_empty_groups);
        expect(submissionStatus.groups_submitted).toBe(submissionStatusData.groups_submitted);
        expect(submissionStatus.submissions_passed).toBe(submissionStatusData.submissions_passed);
    });
});

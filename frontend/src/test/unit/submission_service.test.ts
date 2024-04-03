/* eslint-disable @typescript-eslint/no-unused-vars */
import { describe, it, expect, beforeEach } from 'vitest';
import { useSubmission } from '@/composables/services/submission.service.ts';

const {
    submissions,
    submission,
    getSubmissionByID,
    getSubmissionByProject,
    getSubmissionByGroup,

    createSubmission,
    deleteSubmission,
} = useSubmission();

describe('submissions', (): void => {
    it('gets submissions data by id', async () => {
        await getSubmissionByID('1');
        expect(submission.value).not.toBeNull();
        expect(submission.value?.group).toBeNull();
        expect(submission.value?.files).toEqual([]);
        expect(submission.value?.extra_checks_results).toEqual([]);
        expect(submission.value?.submission_number).toBe(1);
        expect(submission.value?.submission_time).toEqual(
            new Date('July 21, 2024 01:15:00'),
        );
    });

    it('gets submissions data by group', async () => {
        await getSubmissionByGroup('1');
        expect(submissions).not.toBeNull();
        expect(Array.isArray(submissions.value)).toBe(true);
        expect(submissions.value?.length).toBe(2);

        expect(submissions.value?.[0]?.group).toBeNull();
        expect(submissions.value?.[0]?.files).toEqual([]);
        expect(submissions.value?.[0]?.extra_checks_results).toEqual([]);
        expect(submissions.value?.[0]?.submission_number).toBe(1);
        expect(submissions.value?.[0]?.submission_time).toEqual(
            new Date('July 21, 2024 01:15:00'),
        );

        expect(submissions.value?.[1]?.group).toBeNull();
        expect(submissions.value?.[1]?.files).toEqual([]);
        expect(submissions.value?.[1]?.extra_checks_results).toEqual([]);
        expect(submissions.value?.[1]?.submission_number).toBe(2);
        expect(submissions.value?.[1]?.submission_time).toEqual(
            new Date('July 21, 2024 01:15:00'),
        );
    });

    it('gets submissions data by project', async () => {
        await getSubmissionByProject('0');
        expect(submissions).not.toBeNull();
        expect(Array.isArray(submissions.value)).toBe(true);
        expect(submissions.value?.length).toBe(2);

        expect(submissions.value?.[0]?.group).toBeNull();
        expect(submissions.value?.[0]?.files).toEqual([]);
        expect(submissions.value?.[0]?.extra_checks_results).toEqual([]);
        expect(submissions.value?.[0]?.submission_number).toBe(1);
        expect(submissions.value?.[0]?.submission_time).toEqual(
            new Date('July 21, 2024 01:15:00'),
        );

        expect(submissions.value?.[1]?.group).toBeNull();
        expect(submissions.value?.[1]?.files).toEqual([]);
        expect(submissions.value?.[1]?.extra_checks_results).toEqual([]);
        expect(submissions.value?.[1]?.submission_number).toBe(2);
        expect(submissions.value?.[1]?.submission_time).toEqual(
            new Date('July 21, 2024 01:15:00'),
        );
    });
});

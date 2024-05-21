/* eslint-disable @typescript-eslint/no-unused-vars */
import { describe, it, expect } from 'vitest';
import { useSubmission } from '@/composables/services/submission.service.ts';

const { submissions, submission, getSubmissionByID, getSubmissionByProject, getSubmissionByGroup } = useSubmission();

function resetService(): void {
    submission.value = null;
    submissions.value = null;
}

describe('submissions', (): void => {
    it('gets submissions data by id', async () => {
        resetService();

        await getSubmissionByID('1');

        // Only check for the relevant fields passed in the get handler
        expect(submission.value).not.toBeNull();
        expect(submission.value?.submission_number).toEqual(1);
        expect(submission.value?.submission_time).toStrictEqual(new Date('July 21, 2024 01:15:00'));
        expect(submission.value?.is_valid).toEqual(true);
    });

    it('gets submissions data by group', async () => {
        resetService();

        await getSubmissionByGroup('1');
        console.log(JSON.stringify(submissions.value))
        // expect(submissions).not.toBeNull();
        // expect(Array.isArray(submissions.value)).toBe(true);
        // expect(submissions.value?.length).toBe(2);

        // expect(submissions.value?.[0]?.files).toEqual([]);
        // expect(submissions.value?.[0]?.submission_number).toBe(1);
        // expect(submissions.value?.[0]?.submission_time).toEqual(new Date('July 21, 2024 01:15:00'));

        // expect(submissions.value?.[1]?.files).toEqual([]);
        // expect(submissions.value?.[1]?.submission_number).toBe(2);
        // expect(submissions.value?.[1]?.submission_time).toEqual(new Date('July 21, 2024 01:15:00'));
    });

    it('gets submissions data by project', async () => {
        resetService();

        await getSubmissionByProject('0');
        expect(submissions).not.toBeNull();
        expect(Array.isArray(submissions.value)).toBe(true);
        expect(submissions.value?.length).toBe(2);

        expect(submissions.value?.[0]?.id).toEqual('1');
        expect(submissions.value?.[0]?.submission_number).toEqual(1);
        expect(submissions.value?.[0]?.submission_time).toStrictEqual(new Date('July 21, 2024 01:15:00'));
        expect(submissions.value?.[0]?.is_valid).toEqual(true);   

        expect(submissions.value?.[1]?.id).toEqual('2');
        expect(submissions.value?.[1]?.submission_number).toEqual(2);
        expect(submissions.value?.[1]?.submission_time).toStrictEqual(new Date('July 21, 2024 01:15:00'));
        expect(submissions.value?.[1]?.is_valid).toEqual(true);    
    });
});

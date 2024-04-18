/*
import { describe, it, expect } from 'vitest';

import { Submission } from '@/types/submission/Submission.ts';
import { submissionData } from './data';
import { createSubmission } from './helper';

describe('submission type', () => {
    it('create instance of submission with correct properties', () => {
        const submission = createSubmission(submissionData);

        expect(submission).toBeInstanceOf(Submission);
        expect(submission.id).toBe(submissionData.id);
        expect(submission.submission_number).toBe(submissionData.submission_number);
        expect(submission.submission_time).toStrictEqual(submissionData.submission_time);
        expect(submission.files).toStrictEqual(submissionData.files);
    });

    it('create a submission instance from JSON data', () => {
        const submissionJSON = { ...submissionData };
        const submission = Submission.fromJSONCreate(submissionJSON);

        expect(submission).toBeInstanceOf(Submission);
        expect(submission.id).toBe(submissionData.id);
        expect(submission.submission_number).toBe(submissionData.submission_number);
        expect(submission.submission_time).toStrictEqual(submissionData.submission_time);
        expect(submission.files).toStrictEqual(submissionData.files);
    });

});
 */

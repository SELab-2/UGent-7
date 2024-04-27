import { describe, it, expect } from 'vitest';

import { Submission } from '@/types/submission/Submission.ts';
import { submissionData } from './data';
import { createSubmission } from './helper';

describe('submission type', () => {
    it('create instance of submission with correct properties', () => {
        const submission = createSubmission(submissionData);

        expect(submission).toBeInstanceOf(Submission);
        expect(submission.id).toBe(submissionData.id);
        expect(submission.submission_number).toStrictEqual(submissionData.submission_number);
        expect(submission.submission_time).toStrictEqual(submissionData.submission_time);
        expect(submission.files).toStrictEqual(submissionData.files);
        expect(submission.extraCheckResults).toStrictEqual(submissionData.extra_check_results);
        expect(submission.structureCheckResults).toStrictEqual(submissionData.structure_check_results);
        expect(submission.is_valid).toBe(submissionData.is_valid);
    });

    it('create a submission instance from JSON data', () => {
        // const submissionJSON = { ...submissionData };
        // const submission = Submission.fromJSON(submissionJSON);

        // expect(submission).toBeInstanceOf(Submission);
        // expect(submission.id).toBe(submissionData.id);
        // expect(submission.submission_number).toStrictEqual(submissionData.submission_number);
        // expect(submission.submission_time).toStrictEqual(submissionData.submission_time);
        // expect(submission.files).toStrictEqual(submissionData.files);
        // expect(submission.extraCheckResults).toStrictEqual(submissionData.extra_check_results);
        // expect(submission.structureCheckResults).toStrictEqual(submissionData.structure_check_results);
        // expect(submission.is_valid).toBe(submissionData.is_valid);
    });
});

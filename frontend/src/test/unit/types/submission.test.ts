/*
import { describe, it, expect } from 'vitest';

import { Submission } from '@/types/submission/Submission.ts';
import { submissionData } from './data';
import { createSubmission } from './helper';
 */
/* TODO change files to zip */
describe('submission type', () => {
    it('create instance of submission with correct properties', () => {

    });
});
/*
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
        const responseSubmissionJSON = {
            id: 'submission1_id',
            submission_number: 1,
            submission_time: new Date('November 1, 2024 04:20:00'),
            files: [],
            results: [],
            is_valid: true,
        };

        const submission = Submission.fromJSON(responseSubmissionJSON);

        expect(submission).toBeInstanceOf(Submission);
        expect(submission.id).toBe(submissionData.id);
        expect(submission.submission_number).toStrictEqual(submissionData.submission_number);
        expect(submission.submission_time).toStrictEqual(submissionData.submission_time);
        expect(submission.files).toStrictEqual(submissionData.files);
        expect(submission.extraCheckResults).toStrictEqual([]);
        expect(submission.structureCheckResults).toStrictEqual([]);
        expect(submission.is_valid).toBe(submissionData.is_valid);
    });
});
 */

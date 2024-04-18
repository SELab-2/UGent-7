import { ExtraCheckResult } from '@/types/submission/ExtraCheckResult.ts';
import { StructureCheckResult } from '@/types/submission/StructureCheckResult.ts';

export class Submission {
    constructor(
        public id: string,
        public submission_number: number,
        public submission_time: Date,
        public files: File[] = [],
        public extraCheckResults: ExtraCheckResult[] = [],
        public structureCheckResults: StructureCheckResult[] = [],
        public is_valid: boolean,
    ) {}

    /**
     * Check if the submission is passed.
     */
    public isPassed(): boolean {
        return this.isExtraCheckPassed() && this.isStructureCheckPassed();
    }

    /**
     * Check if some of the checks is passed.
     */
    public isSomePassed(): boolean {
        return this.isExtraCheckPassed() || this.isStructureCheckPassed();
    }

    /**
     * Check if the extra check is passed.
     */
    public isExtraCheckPassed(): boolean {
        const extraChecksPassed = this.extraCheckResults.map((check: ExtraCheckResult) => check.result === 'SUCCESS');
        return extraChecksPassed.every((check: boolean) => check);
    }

    /**
     * Check if the structure check is passed.
     */
    public isStructureCheckPassed(): boolean {
        const structureChecksPassed = this.structureCheckResults.map(
            (check: StructureCheckResult) => check.result === 'SUCCESS',
        );
        return structureChecksPassed.every((check: boolean) => check);
    }

    /**
     * Convert a submission object to a submission instance.
     *
     * @param submission
     */
    static fromJSON(submission: ResponseSubmission): Submission {
        const extraCheckResults = submission.results
            .filter((result: any) => result.resourcetype === 'ExtraCheckResult')
            .map((result: ExtraCheckResult) => ExtraCheckResult.fromJSON(result));

        const structureCheckResult = submission.results
            .filter((result: any) => result.resourcetype === 'StructureCheckResult')
            .map((result: StructureCheckResult) => StructureCheckResult.fromJSON(result));
        return new Submission(
            submission.id,
            submission.submission_number,
            new Date(submission.submission_time),
            submission.files,
            extraCheckResults,
            structureCheckResult,
            submission.is_valid,
        );
    }

    static fromJSONCreate(respons: { message: string; submission: ResponseSubmission }): Submission {
        return Submission.fromJSON(respons.submission);
    }
}

class ResponseSubmission {
    constructor(
        public id: string,
        public submission_number: number,
        public submission_time: Date,
        public files: File[] = [],
        public results: any[],
        public is_valid: boolean,
    ) {}
}

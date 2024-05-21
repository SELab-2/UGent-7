import { ExtraCheckResult, type ExtraCheckResultJSON } from '@/types/submission/ExtraCheckResult.ts';
import { StructureCheckResult, type StructureCheckResultJSON } from '@/types/submission/StructureCheckResult.ts';
import { type HyperlinkedRelation } from '@/types/ApiResponse.ts';

export interface SubmissionJSON {
    id: string;
    submission_number: number;
    submission_time: string;
    is_valid: boolean;
    zip: HyperlinkedRelation;
    group: HyperlinkedRelation;
    results: Array<ExtraCheckResultJSON | StructureCheckResultJSON>;
}

export class Submission {
    constructor(
        public id: string = '',
        public submission_number: number = 0,
        public submission_time: Date = new Date(),
        public is_valid: boolean = false,
        public extraCheckResults: ExtraCheckResult[] = [],
        public structureCheckResults: StructureCheckResult[] = [],
        public zip: File | null = null,
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
    static fromJSON(submission: SubmissionJSON): Submission {
        const extraCheckResults = submission.results
            .filter(
                (result: ExtraCheckResultJSON | StructureCheckResultJSON) => result.resourcetype === 'ExtraCheckResult',
            )
            .map((result: any) => ExtraCheckResult.fromJSON(result as ExtraCheckResultJSON));

        const structureCheckResults = submission.results
            .filter(
                (result: ExtraCheckResultJSON | StructureCheckResultJSON) =>
                    result.resourcetype === 'StructureCheckResult',
            )
            .map((result: any) => StructureCheckResult.fromJSON(result as StructureCheckResultJSON));

        return new Submission(
            submission.id,
            submission.submission_number,
            new Date(submission.submission_time),
            submission.is_valid,
            extraCheckResults,
            structureCheckResults,
        );
    }
}

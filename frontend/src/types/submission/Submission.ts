import { type ExtraCheckResult } from '@/types/submission/ExtraCheckResult.ts';
import { type StructureCheckResult } from '@/types/submission/StructureCheckResult.ts';

export class Submission {
    constructor(
        public id: string,
        public submission_number: number,
        public submission_time: Date,
        public files: File[] = [],
        public extraCheckResults: ExtraCheckResult[] = [],
        public structureCheckResult: StructureCheckResult[] = [],
    ) {}

    /**
     * Convert a submission object to a submission instance.
     *
     * @param submission
     */
    static fromJSON(submission: Submission): Submission {
        return new Submission(
            submission.id,
            submission.submission_number,
            new Date(submission.submission_time),
            submission.files,
        );
    }
}

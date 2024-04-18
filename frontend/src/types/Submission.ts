import { type Group } from './Group';

export class Submission {
    constructor(
        public id: string,
        public submission_number: number,
        public submission_time: Date,
        public structure_checks_passed: boolean,
        public group: Group | null = null,
        public files: File[] | null = null, // TODO check
        public extra_checks_results: any[] | null = null, // TODO
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
            submission.structure_checks_passed,
        );
    }
}

import { Group } from "./Group";

export class Submission {
    constructor(
        public id: number,
        public submission_number: number,
        public submission_time: Date,
        public structure_checks_passed: boolean,
        public group: Group = new Group(0),
        public files: File[] = [], //TODO check
        public extra_checks_results : any[] = [], // TODO

    ) {
    }

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
            submission.structure_checks_passed
        )
    }
}
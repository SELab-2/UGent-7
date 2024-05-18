export class SubmissionStatus {
    constructor(
        public non_empty_groups: number = 0,
        public groups_submitted: number = 0,
        public submissions_passed: number = 0,
    ) {}

    /**
     * Convert a submissionStatus object to a submissionStatus instance.
     *
     * @param submissionStatus
     */
    static fromJSON(submissionStatus: SubmissionStatus): SubmissionStatus {
        return new SubmissionStatus(
            submissionStatus.non_empty_groups,
            submissionStatus.groups_submitted,
            submissionStatus.submissions_passed,
        );
    }
}

export class SubmissionStatus {
    constructor(
        public non_empty_groups: number,
        public groups_submitted: number,
        public structure_checks_passed: number,
        public extra_checks_passed: number,
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
            submissionStatus.structure_checks_passed,
            submissionStatus.extra_checks_passed,
        );
    }
}

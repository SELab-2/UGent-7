export interface SubmissionStatusJSON {
    non_empty_groups: number;
    groups_submitted: number;
    has_structure_checks: boolean;
    has_extra_checks: boolean;
    structure_checks_passed: number;
    extra_checks_passed: number;
}

export class SubmissionStatus {
    constructor(
        public non_empty_groups: number = 0,
        public groups_submitted: number = 0,
        public has_structure_checks: boolean = false,
        public has_extra_checks: boolean = false,
        public structure_checks_passed: number = 0,
        public extra_checks_passed: number = 0,
    ) {}

    /**
     * Convert a submissionStatus object to a submissionStatus instance.
     *
     * @param submissionStatus
     */
    static fromJSON(submissionStatus: SubmissionStatusJSON): SubmissionStatus {
        return new SubmissionStatus(
            submissionStatus.non_empty_groups,
            submissionStatus.groups_submitted,
            submissionStatus.has_structure_checks,
            submissionStatus.has_extra_checks,
            submissionStatus.structure_checks_passed,
            submissionStatus.extra_checks_passed,
        );
    }
}

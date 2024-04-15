export class ExtraCheckResult {
    constructor(
        public id: string,
        public result: any,
        public error_message: any,
        public is_valid: boolean,
        public log_file: File,
        public submission_id: number,
        public extra_check_id: number,
    ) {}

    static fromJSON(extraCheckResult: ExtraCheckResult): ExtraCheckResult {
        return new ExtraCheckResult(
            extraCheckResult.id,
            extraCheckResult.result,
            extraCheckResult.error_message,
            extraCheckResult.is_valid,
            extraCheckResult.log_file,
            extraCheckResult.submission_id,
            extraCheckResult.extra_check_id,
        );
    }
}

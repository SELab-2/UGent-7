export class ExtraCheckResult {
    constructor(
        public id: string,
        public result: string,
        public error_message: any,
        public log_file: string,
        public artifact: string,
        public submission: number,
        public extra_check: number,
        public resourcetype: string,
    ) {}

    static fromJSON(extraCheckResult: ExtraCheckResult): ExtraCheckResult {
        return new ExtraCheckResult(
            extraCheckResult.id,
            extraCheckResult.result,
            extraCheckResult.error_message,
            extraCheckResult.log_file,
            extraCheckResult.artifact,
            extraCheckResult.submission,
            extraCheckResult.extra_check,
            extraCheckResult.resourcetype,
        );
    }
}

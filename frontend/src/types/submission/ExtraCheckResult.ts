import { Submission } from '@/types/submission/Submission.ts';
import { ExtraCheck } from '@/types/ExtraCheck.ts';
import { type HyperlinkedRelation } from '@/types/ApiResponse.ts';

export interface ExtraCheckResultJSON {
    id: string;
    result: string;
    error_message: string | null;
    submission: number;
    structure_check: number;
    resourcetype: string;
    log_file: HyperlinkedRelation;
    artifact: HyperlinkedRelation;
}

export class ExtraCheckResult {
    constructor(
        public id: string = '',
        public result: string = '',
        public error_message: any | null = null,
        public log_file: string = '',
        public artifact: string = '',
        public submission: number = 0,
        public extra_check: number = 0,
        public resourcetype: string = '',
    ) {}

    static fromJSON(extraCheckResult: ExtraCheckResultJSON): ExtraCheckResult {
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

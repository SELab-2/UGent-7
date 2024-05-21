import { Submission } from '@/types/submission/Submission.ts';
import { ExtraCheck } from '@/types/ExtraCheck.ts';
import { HyperlinkedRelation } from '@/types/ApiResponse.ts';

export type ExtraCheckResultJSON = {
    id: string;
    result: string;
    error_message: string|null;
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
        public error_message: string|null = null,
        public resourcetype: string = '',
        public submission: Submission = new Submission(),
        public extra_check: ExtraCheck = new ExtraCheck(),
    ) {}

    static fromJSON(extraCheckResult: ExtraCheckResultJSON): ExtraCheckResult {
        return new ExtraCheckResult(
            extraCheckResult.id,
            extraCheckResult.result,
            extraCheckResult.error_message,
            extraCheckResult.resourcetype,
        );
    }
}

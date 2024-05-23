import { type HyperlinkedRelation } from '@/types/ApiResponse.ts';
import { StructureCheck } from '@/types/StructureCheck.ts';
import { Submission } from '@/types/submission/Submission.ts';

export interface StructureCheckResultJSON {
    id: string;
    result: string;
    error_message: string;
    submission: number;
    structure_check: number;
    resourcetype: string;
    log_file: HyperlinkedRelation;
    artifact: HyperlinkedRelation;
}

export class StructureCheckResult {
    constructor(
        public id: string = '',
        public result: string = '',
        public error_message: string = '',
        public resourcetype: string = '',
        public submission: Submission = new Submission(),
        public structure_check: StructureCheck = new StructureCheck(),
    ) {}

    static fromJSON(structureCheckResult: StructureCheckResultJSON): StructureCheckResult {
        return new StructureCheckResult(
            structureCheckResult.id,
            structureCheckResult.result,
            structureCheckResult.error_message,
            structureCheckResult.resourcetype,
        );
    }
}

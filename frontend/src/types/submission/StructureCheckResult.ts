export class StructureCheckResult {
    constructor(
        public id: string,
        public result: any,
        public error_message: any,
        public is_valid: boolean,
        public submission_id: number,
        public structure_check_id: number,
    ) {}

    static fromJSON(structureCheckResult: StructureCheckResult): StructureCheckResult {
        return new StructureCheckResult(
            structureCheckResult.id,
            structureCheckResult.result,
            structureCheckResult.error_message,
            structureCheckResult.is_valid,
            structureCheckResult.submission_id,
            structureCheckResult.structure_check_id,
        );
    }
}

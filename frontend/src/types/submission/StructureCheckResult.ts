export class StructureCheckResult {
    constructor(
        public id: string,
        public result: string,
        public error_message: any,
        public submission: number,
        public structure_check: number,
        public resourcetype: string,
    ) {}

    static fromJSON(structureCheckResult: StructureCheckResult): StructureCheckResult {
        return new StructureCheckResult(
            structureCheckResult.id,
            structureCheckResult.result,
            structureCheckResult.error_message,
            structureCheckResult.submission,
            structureCheckResult.structure_check,
            structureCheckResult.resourcetype,
        );
    }
}

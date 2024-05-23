import { describe, it, expect } from 'vitest';

import { StructureCheckResult } from '@/types/submission/StructureCheckResult';
import { structureCheckResultData } from './data';
import { createStructureCheckResult } from './helper';

describe('structureCheckResult type', () => {
    it('create instance of structureCheckData with correct properties', () => {
        const structureCheckResult = createStructureCheckResult(structureCheckResultData);

        expect(structureCheckResult).toBeInstanceOf(StructureCheckResult);
        expect(structureCheckResult.id).toBe(structureCheckResultData.id);
        expect(structureCheckResult.result).toBe(structureCheckResultData.result);
        expect(structureCheckResult.error_message).toBe(structureCheckResultData.error_message);
        expect(structureCheckResult.submission).toBe(structureCheckResultData.submission);
        expect(structureCheckResult.structure_check).toBe(structureCheckResultData.structure_check);
        expect(structureCheckResult.resourcetype).toBe(structureCheckResultData.resourcetype);
    });

    it('create a structureCheckResult instance from JSON data', () => {
        const structureCheckResultJSON = { ...structureCheckResultData };
        const structureCheckResult = StructureCheckResult.fromJSON(structureCheckResultJSON);

        expect(structureCheckResult).toBeInstanceOf(StructureCheckResult);
        expect(structureCheckResult.id).toBe(structureCheckResultData.id);
        expect(structureCheckResult.result).toBe(structureCheckResultData.result);
        expect(structureCheckResult.error_message).toBe(structureCheckResultData.error_message);
        expect(structureCheckResult.submission).toBe(structureCheckResultData.submission);
        expect(structureCheckResult.structure_check).toBe(structureCheckResultData.structure_check);
        expect(structureCheckResult.resourcetype).toBe(structureCheckResultData.resourcetype);
    });
});

import { describe, it, expect } from 'vitest';

import { StructureCheck } from '@/types/StructureCheck';
import { structureCheckData } from './data';
import { createStructureCheck } from './helper';

describe('structureCheck type', () => {
    it('create instance of structureCheck with correct properties', () => {
        const structureCheck = createStructureCheck(structureCheckData);

        expect(structureCheck).toBeInstanceOf(StructureCheck);
        expect(structureCheck.id).toBe(structureCheckData.id);
        expect(structureCheck.name).toBe(structureCheckData.name);
        expect(structureCheck.obligated_extensions).toStrictEqual(structureCheckData.obligated_extensions);
        expect(structureCheck.blocked_extensions).toStrictEqual(structureCheckData.blocked_extensions);
        expect(structureCheck.project).toStrictEqual(structureCheckData.project);
    });

    it('create a structureCheck instance from JSON data', () => {
        const structureCheckJSON = { ...structureCheckData };
        const structureCheck = StructureCheck.fromJSON(structureCheckJSON);

        expect(structureCheck).toBeInstanceOf(StructureCheck);
        expect(structureCheck.id).toBe(structureCheckData.id);
        expect(structureCheck.name).toBe(structureCheckData.name);
        expect(structureCheck.obligated_extensions).toStrictEqual(structureCheckData.obligated_extensions);
        expect(structureCheck.blocked_extensions).toStrictEqual(structureCheckData.blocked_extensions);
        expect(structureCheck.project).toStrictEqual(structureCheckData.project);
    });
});

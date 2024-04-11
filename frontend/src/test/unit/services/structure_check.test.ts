/* eslint-disable @typescript-eslint/no-unused-vars */
import { describe, it, expect } from 'vitest';
import { useStructureCheck } from '@/composables/services/structure_check.service.ts';

const { 
    structureChecks,
    structureCheck,
    getStructureCheckByID,
    getStructureCheckByProject,

    createStructureCheck,
    deleteStructureCheck,
 } = useStructureCheck();

describe('structureCheck', (): void => {
    it('gets structure check data by id', async () => {
        await getStructureCheckByID('1');
        expect(structureCheck.value).not.toBeNull();
        expect(structureCheck.value?.name).toBe('.');
        expect(structureCheck.value?.project).toBeNull();
        expect(structureCheck.value?.name).toBe('.');
        expect(structureCheck.value?.name).toBe('.');
    });

    it('gets structureCheck data', async () => {
        await getStructureCheckByProject('123456');
        expect(structureChecks).not.toBeNull();
        expect(Array.isArray(structureChecks.value)).toBe(true);
        expect(structureChecks.value?.length).toBe(4);
        expect(structureChecks.value).not.toBeNull();

        expect(structureChecks.value?.[0]?.name).toBe('.');
        expect(structureChecks.value?.[0]?.project).toBeNull();
        expect(structureChecks.value?.[0]?.obligated_extensions).toEqual([]);
        expect(structureChecks.value?.[0]?.blocked_extensions).toEqual([]);

        expect(structureChecks.value?.[1]?.name).toBe('folder1');
        expect(structureChecks.value?.[1]?.project).toBeNull();
        expect(structureChecks.value?.[1]?.obligated_extensions).toEqual([]);
        expect(structureChecks.value?.[1]?.blocked_extensions).toEqual([]);

        expect(structureChecks.value?.[2]?.name).toBe('folder3');
        expect(structureChecks.value?.[2]?.project).toBeNull();
        expect(structureChecks.value?.[2]?.obligated_extensions).toEqual([]);
        expect(structureChecks.value?.[2]?.blocked_extensions).toEqual([]);

        expect(structureChecks.value?.[3]?.name).toBe('folder3/folder3-1');
        expect(structureChecks.value?.[3]?.project).toBeNull();
        expect(structureChecks.value?.[3]?.obligated_extensions).toEqual([]);
        expect(structureChecks.value?.[3]?.blocked_extensions).toEqual([]);
    });
});

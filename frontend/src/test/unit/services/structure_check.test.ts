/* eslint-disable @typescript-eslint/no-unused-vars */
import { describe, it, expect } from 'vitest';
import { useStructureCheck } from '@/composables/services/structure_check.service.ts';

const { structureChecks, structureCheck, getStructureCheckByID } = useStructureCheck();

function resetService(): void {
    structureCheck.value = null;
    structureChecks.value = null;
}

describe('structureCheck', (): void => {
    it('gets structure check data by id', async () => {
        resetService();

        await getStructureCheckByID('1');
        expect(structureCheck.value).not.toBeNull();
        expect(structureCheck.value?.path).toBe('.');
    });

    // it('gets structureCheck data', async () => {
    //     resetService();
    //
    //     await getStructureCheckByProject('123456');
    //     expect(structureChecks).not.toBeNull();
    //     expect(Array.isArray(structureChecks.value)).toBe(true);
    //     expect(structureChecks.value?.length).toBe(4);
    //     expect(structureChecks.value).not.toBeNull();
    //
    //     expect(structureChecks.value?.[0]?.path).toBe('.');
    //     expect(structureChecks.value?.[0]?.project).toBeNull();
    //     expect(structureChecks.value?.[0]?.obligated_extensions).toEqual([]);
    //     expect(structureChecks.value?.[0]?.blocked_extensions).toEqual([]);
    //
    //     expect(structureChecks.value?.[1]?.path).toBe('folder1');
    //     expect(structureChecks.value?.[1]?.project).toBeNull();
    //     expect(structureChecks.value?.[1]?.obligated_extensions).toEqual([]);
    //     expect(structureChecks.value?.[1]?.blocked_extensions).toEqual([]);
    //
    //     expect(structureChecks.value?.[2]?.path).toBe('folder3');
    //     expect(structureChecks.value?.[2]?.project).toBeNull();
    //     expect(structureChecks.value?.[2]?.obligated_extensions).toEqual([]);
    //     expect(structureChecks.value?.[2]?.blocked_extensions).toEqual([]);
    //
    //     expect(structureChecks.value?.[3]?.path).toBe('folder3/folder3-1');
    //     expect(structureChecks.value?.[3]?.project).toBeNull();
    //     expect(structureChecks.value?.[3]?.obligated_extensions).toEqual([]);
    //     expect(structureChecks.value?.[3]?.blocked_extensions).toEqual([]);
    // });
});

// it('create structureCheck', async () => {
//     resetService();
//
//     const exampleStructureCheck = new StructureCheck(
//         '', // id
//         'structure_check_name', // name
//     );
//
//     await getStructureCheckByProject('123456');
//     expect(structureChecks).not.toBeNull();
//     expect(Array.isArray(structureChecks.value)).toBe(true);
//     const prevLength = structureChecks.value?.length ?? 0;
//
//     await createStructureCheck(exampleStructureCheck, '123456');
//     await getStructureCheckByProject('123456');
//
//     expect(structureChecks).not.toBeNull();
//     expect(Array.isArray(structureChecks.value)).toBe(true);
//     expect(structureChecks.value?.length).toBe(prevLength + 1);
//
//     // Only check for fields that are sent to the backend
//     expect(structureChecks.value?.[prevLength]?.path).toBe('structure_check_name');
// });
//
// it('delete structureCheck', async () => {
//     resetService();
//
//     await getStructureCheckByProject('123456');
//     expect(structureChecks.value).not.toBeNull();
//     expect(Array.isArray(structureChecks.value)).toBe(true);
//     const prevLength = structureChecks.value?.length ?? 0;
//
//     let structureCheckId = '';
//     if (structureChecks.value?.[2]?.id !== undefined && structureChecks.value?.[2].id !== null) {
//         structureCheckId = structureChecks.value?.[2]?.id;
//     }
//
//     await deleteStructureCheck(structureCheckId);
//     await getStructureCheckByProject('123456');
//
//     expect(structureChecks).not.toBeNull();
//     expect(Array.isArray(structureChecks.value)).toBe(true);
//     expect(structureChecks.value?.length).toBe(prevLength - 1);
//     expect(structureChecks.value?.[2]?.id).not.toBe(structureCheckId);
// });

import {describe, it, expect, beforeEach} from 'vitest'
import { useStructureCheck } from '@/composables/services/structure_check.service.ts'

const {
    structure_checks,
    structure_check,
    getStructureCheckByID,
    getStructureCheckByProject,

    createStructureCheck,
    deleteStructureCheck
} = useStructureCheck();

describe("structure_check", (): void => {
    it("gets structure check data by id", async () => {
        await getStructureCheckByID("1")
        expect(structure_check.value).not.toBeNull()
        expect(structure_check.value?.name).toBe(".")
        expect(structure_check.value?.project).toBeNull()
        expect(structure_check.value?.name).toBe(".")
        expect(structure_check.value?.name).toBe(".")
    })

    it("gets admins data", async () => {
        await getStructureCheckByProject("123456")
        expect(structure_checks).not.toBeNull()
        expect(Array.isArray(structure_checks.value)).toBe(true)
        expect(structure_checks.value?.length).toBe(4);
        expect(structure_checks.value).not.toBeNull()

        expect(structure_checks.value?.[0]?.name).toBe(".")
        expect(structure_checks.value?.[0]?.project).toBeNull()
        expect(structure_checks.value?.[0]?.obligated_extensions).toEqual([])
        expect(structure_checks.value?.[0]?.blocked_extensions).toEqual([])

        expect(structure_checks.value?.[1]?.name).toBe("folder1")
        expect(structure_checks.value?.[1]?.project).toBeNull()
        expect(structure_checks.value?.[1]?.obligated_extensions).toEqual([])
        expect(structure_checks.value?.[1]?.blocked_extensions).toEqual([])

        expect(structure_checks.value?.[2]?.name).toBe("folder3")
        expect(structure_checks.value?.[2]?.project).toBeNull()
        expect(structure_checks.value?.[2]?.obligated_extensions).toEqual([])
        expect(structure_checks.value?.[2]?.blocked_extensions).toEqual([])

        expect(structure_checks.value?.[3]?.name).toBe("folder3/folder3-1")
        expect(structure_checks.value?.[3]?.project).toBeNull()
        expect(structure_checks.value?.[3]?.obligated_extensions).toEqual([])
        expect(structure_checks.value?.[3]?.blocked_extensions).toEqual([])
    })
})
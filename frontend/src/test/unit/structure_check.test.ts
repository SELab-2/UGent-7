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
   /*
    it("gets admins data", async () => {
        await getAdmins()
        expect(admins).not.toBeNull()
        expect(Array.isArray(admins.value)).toBe(true)
        expect(admins.value?.length).toBe(2);

        expect(admins.value?.[0]?.username).toBe("tverslyp")
        expect(admins.value?.[0]?.is_staff).toBe(true)
        expect(admins.value?.[0]?.email).toBe("Tybo.Verslype@UGent.be")
        expect(admins.value?.[0]?.first_name).toBe("Tybo")
        expect(admins.value?.[0]?.last_name).toBe("Verslype")
        expect(admins.value?.[0]?.last_enrolled).toBe(2023)
        expect(admins.value?.[0]?.last_login).toEqual(new Date("July 23, 2024 01:15:00"))
        expect(admins.value?.[0]?.create_time).toEqual(new Date("July 21, 2024 01:15:00"))
        expect(admins.value?.[0]?.faculties).toEqual([])

        expect(admins.value?.[1]?.username).toBe("simmig")
        expect(admins.value?.[1]?.is_staff).toBe(true)
        expect(admins.value?.[1]?.email).toBe("Simon.Mignolet@UGent.be")
        expect(admins.value?.[1]?.first_name).toBe("Simon")
        expect(admins.value?.[1]?.last_name).toBe("Mignolet")
        expect(admins.value?.[1]?.last_enrolled).toBe(2023)
        expect(admins.value?.[0]?.last_login).toEqual(new Date("July 23, 2024 01:15:00"))
        expect(admins.value?.[0]?.create_time).toEqual(new Date("July 21, 2024 01:15:00"))
        expect(admins.value?.[1]?.faculties).toEqual([])
    })
    */
})
import {describe, it, expect, beforeEach} from 'vitest'
import { useFaculty } from '@/composables/services/faculties.service.ts'

const {
    faculties,
    faculty,
    getFacultyByID,
    getFacultys,

    createFaculty,
    deleteFaculty
} = useFaculty();

describe("faculty", (): void => {
    it("gets faculty data by id", async () => {
        await getFacultyByID("wetenschappen")
        expect(faculty.value).not.toBeNull()
        expect(faculty.value?.name).toBe("wetenschappen")
    })

    it("gets faculties data", async () => {
        await getFacultys()
        expect(faculties).not.toBeNull()
        expect(Array.isArray(faculties.value)).toBe(true)
        expect(faculties.value?.length).toBe(2);
        expect(faculties.value?.[0]).not.toBeNull()
        expect(faculties.value?.[0].name).toBe("wetenschappen")
        expect(faculties.value?.[1]).not.toBeNull()
        expect(faculties.value?.[1].name).toBe("voetbal")
    })
})
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
        await getFacultyByID("0")
        expect(faculty.value).not.toBeNull()
        expect(faculty.value?.name).toBe("wetenschappen")
    })
})
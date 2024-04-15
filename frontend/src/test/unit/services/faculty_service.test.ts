/* eslint-disable @typescript-eslint/no-unused-vars */
import { describe, it, expect } from 'vitest';
import { useFaculty } from '@/composables/services/faculty.service.ts';
import { Faculty } from '@/types/Faculty';

const {
    faculties,
    faculty,
    getFacultyByID,
    getFaculties,

    createFaculty,
    deleteFaculty,
} = useFaculty();

function resetService(): void {
    faculty.value = null;
    faculties.value = null;
}

describe('faculty', (): void => {
    it('gets faculty data by id', async () => {
        resetService();

        await getFacultyByID('sciences');
        expect(faculty.value).not.toBeNull();
        expect(faculty.value?.name).toBe('wetenschappen');
    });

    it('gets faculties data', async () => {
        resetService();

        await getFaculties();
        expect(faculties).not.toBeNull();
        expect(Array.isArray(faculties.value)).toBe(true);
        expect(faculties.value?.length).toBe(2);
        expect(faculties.value?.[0]).not.toBeNull();
        expect(faculties.value?.[0].name).toBe('wetenschappen');
        expect(faculties.value?.[1]).not.toBeNull();
        expect(faculties.value?.[1].name).toBe('voetbal');
    });

    it('create faculty', async () => {
        resetService();

        const exampleFaculty = new Faculty(
            'faculty_id', // id
            'faculty_name', // name
        );

        await getFaculties();
        expect(faculties).not.toBeNull();
        expect(Array.isArray(faculties.value)).toBe(true);
        const prevLength = faculties.value?.length ?? 0;

        await createFaculty(exampleFaculty);
        await getFaculties();

        expect(faculties).not.toBeNull();
        expect(Array.isArray(faculties.value)).toBe(true);
        expect(faculties.value?.length).toBe(prevLength + 1);

        // Only check for fields that are sent to the backend
        expect(faculties.value?.[prevLength]?.id).toBe('faculty_id');
        expect(faculties.value?.[prevLength]?.name).toBe('faculty_name');
    });
});

import { describe, it, expect } from 'vitest';

import { Faculty } from '@/types/Faculty';
import { facultyData } from './data';
import { createFaculty } from './helper';

describe('faculty type', () => {
    it('create instance of faculty with correct properties', () => {
        const faculty = createFaculty(facultyData);

        expect(faculty).toBeInstanceOf(Faculty);
        expect(faculty.id).toBe(facultyData.id);
        expect(faculty.name).toBe(facultyData.name);
    });

    it('create a faculty instance from JSON data', () => {
        const facultyJSON = { ...facultyData };
        const faculty = Faculty.fromJSON(facultyJSON);

        expect(faculty).toBeInstanceOf(Faculty);
        expect(faculty.id).toBe(facultyData.id);
        expect(faculty.name).toBe(facultyData.name);
    });
});

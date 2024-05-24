import { describe, it, expect } from 'vitest';

import { Teacher } from '@/types/users/Teacher';
import { teacherData } from './data';
import { createTeacher } from './helper';

describe('teacher type', () => {
    it('create instance of teacher with correct properties', () => {
        const teacher = createTeacher(teacherData);

        expect(teacher).toBeInstanceOf(Teacher);
        expect(teacher.id).toBe(teacherData.id);
        expect(teacher.username).toBe(teacherData.username);
        expect(teacher.email).toBe(teacherData.email);
        expect(teacher.first_name).toBe(teacherData.first_name);
        expect(teacher.last_name).toBe(teacherData.last_name);
        expect(teacher.last_enrolled).toBe(teacherData.last_enrolled);
        expect(teacher.roles).toStrictEqual(teacherData.roles);
        expect(teacher.faculties).toStrictEqual(teacherData.faculties);
        expect(teacher.courses).toStrictEqual(teacherData.courses);
        expect(teacher.create_time).toStrictEqual(teacherData.create_time);
        expect(teacher.last_login).toStrictEqual(teacherData.last_login);
    });

    // it('create a teacher instance from JSON data', () => {
    //     const teacherJSON = { ...teacherData };
    //     const teacher = Teacher.fromJSON(teacherJSON);
    //
    //     expect(teacher).toBeInstanceOf(Teacher);
    //     expect(teacher.id).toBe(teacherData.id);
    //     expect(teacher.username).toBe(teacherData.username);
    //     expect(teacher.email).toBe(teacherData.email);
    //     expect(teacher.first_name).toBe(teacherData.first_name);
    //     expect(teacher.last_name).toBe(teacherData.last_name);
    //     expect(teacher.last_enrolled).toBe(teacherData.last_enrolled);
    //     expect(teacher.roles).toStrictEqual(teacherData.roles);
    //     expect(teacher.faculties).toStrictEqual(teacherData.faculties);
    //     expect(teacher.courses).toStrictEqual(teacherData.courses);
    //     expect(teacher.create_time).toStrictEqual(teacherData.create_time);
    //     expect(teacher.last_login).toStrictEqual(teacherData.last_login);
    // });

    it('return true when isTeacher method is called', () => {
        const teacher = createTeacher(teacherData);

        expect(teacher.isTeacher()).toBe(true);
    });
});

import { describe, it, expect } from 'vitest';

import { Student } from '@/types/users/Student';
import { studentData } from './data';
import { createStudent } from './helper';

describe('student type', () => {
    it('create instance of student with correct properties', () => {
        const student = createStudent(studentData);

        expect(student).toBeInstanceOf(Student);
        expect(student.id).toBe(studentData.id);
        expect(student.username).toBe(studentData.username);
        expect(student.email).toBe(studentData.email);
        expect(student.first_name).toBe(studentData.first_name);
        expect(student.last_name).toBe(studentData.last_name);
        expect(student.is_staff).toBe(studentData.is_staff);
        expect(student.last_enrolled).toBe(studentData.last_enrolled);
        expect(student.create_time).toStrictEqual(studentData.create_time);
        expect(student.last_login).toStrictEqual(studentData.last_login);
        expect(student.student_id).toBe(studentData.student_id);
        expect(student.roles).toStrictEqual(studentData.roles);
        expect(student.courses).toStrictEqual(studentData.courses);
        expect(student.groups).toStrictEqual(studentData.groups);
        expect(student.faculties).toStrictEqual(studentData.faculties);
    });

    it('create a student instance from JSON data', () => {
        const studentJSON = { ...studentData };
        const student = Student.fromJSON(studentJSON);

        expect(student).toBeInstanceOf(Student);
        expect(student.id).toBe(studentData.id);
        expect(student.username).toBe(studentData.username);
        expect(student.email).toBe(studentData.email);
        expect(student.first_name).toBe(studentData.first_name);
        expect(student.last_name).toBe(studentData.last_name);
        expect(student.is_staff).toBe(studentData.is_staff);
        expect(student.last_enrolled).toBe(studentData.last_enrolled);
        expect(student.create_time).toStrictEqual(studentData.create_time);
        expect(student.last_login).toStrictEqual(studentData.last_login);
        expect(student.student_id).toBe(studentData.student_id);
        expect(student.roles).toStrictEqual(studentData.roles);
        expect(student.courses).toStrictEqual(studentData.courses);
        expect(student.groups).toStrictEqual(studentData.groups);
        expect(student.faculties).toStrictEqual(studentData.faculties);
    });

    it('return true when isStudent method is called', () => {
        const student = createStudent(studentData);

        expect(student.isStudent()).toBe(true);
    });
});

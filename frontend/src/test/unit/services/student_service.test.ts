/* eslint-disable @typescript-eslint/no-unused-vars */
import { describe, it, expect } from 'vitest';
import { useStudents } from '@/composables/services/students.service.ts';
import { Student } from '@/types/users/Student';

const {
    students,
    student,

    getStudentByID,
    getStudents,
    getStudentsByCourse,
    getStudentsByGroup,

    createStudent,
    deleteStudent,

    studentJoinCourse,
    studentLeaveCourse,
    studentJoinGroup,
    studentLeaveGroup,
} = useStudents();

describe('students', (): void => {
    it('gets student data by id', async () => {
        await getStudentByID('1');
        expect(student.value).not.toBeNull();
        expect(student.value?.username).toBe('jdoe');
        expect(student.value?.is_staff).toBe(false);
        expect(student.value?.email).toBe('John.Doe@hotmail.com');
        expect(student.value?.first_name).toBe('John');
        expect(student.value?.last_name).toBe('Doe');
        expect(student.value?.last_enrolled).toBe(2023);
        expect(student.value?.studentId).toBeNull();
        expect(student.value?.last_login).toBeNull();
        expect(student.value?.create_time.toISOString()).toEqual('2024-07-20T23:15:00.000Z');
        expect(student.value?.courses).toEqual([]);
        expect(student.value?.groups).toEqual([]);
        expect(student.value?.faculties).toEqual([]);
    });

    it('gets students data', async () => {
        await getStudents();
        expect(students).not.toBeNull();
        expect(Array.isArray(students.value)).toBe(true);
        expect(students.value?.length).toBe(4);

        expect(students.value?.[0]?.username).toBe('jdoe');
        expect(students.value?.[0]?.is_staff).toBe(false);
        expect(students.value?.[0]?.email).toBe('John.Doe@hotmail.com');
        expect(students.value?.[0]?.first_name).toBe('John');
        expect(students.value?.[0]?.last_name).toBe('Doe');
        expect(students.value?.[0]?.last_enrolled).toBe(2023);
        expect(students.value?.[0]?.studentId).toBeNull();
        expect(students.value?.[0]?.last_login).toBeNull();
        expect(students.value?.[0]?.create_time).toEqual(new Date('July 21, 2024 01:15:00'));
        expect(students.value?.[0]?.courses).toEqual([]);
        expect(students.value?.[0]?.groups).toEqual([]);
        expect(students.value?.[0]?.faculties).toEqual([]);

        expect(students.value?.[1]?.username).toBe('bverhae');
        expect(students.value?.[1]?.is_staff).toBe(false);
        expect(students.value?.[1]?.email).toBe('Bartje.Verhaege@gmail.com');
        expect(students.value?.[1]?.first_name).toBe('Bartje');
        expect(students.value?.[1]?.last_name).toBe('Verhaege');
        expect(students.value?.[1]?.last_enrolled).toBe(2023);
        expect(students.value?.[1]?.studentId).toBeNull();
        expect(students.value?.[1]?.last_login).toBeNull();
        expect(students.value?.[1]?.create_time).toEqual(new Date('July 21, 2024 01:15:00'));
        expect(students.value?.[1]?.courses).toEqual([]);
        expect(students.value?.[1]?.groups).toEqual([]);
        expect(students.value?.[1]?.faculties).toEqual([]);

        expect(students.value?.[2]?.username).toBe('tverslyp');
        expect(students.value?.[2]?.is_staff).toBe(true);
        expect(students.value?.[2]?.email).toBe('Tybo.Verslype@UGent.be');
        expect(students.value?.[2]?.first_name).toBe('Tybo');
        expect(students.value?.[2]?.last_name).toBe('Verslype');
        expect(students.value?.[2]?.last_enrolled).toBe(2023);
        expect(students.value?.[2]?.studentId).toBe('02012470');
        expect(students.value?.[2]?.last_login).toEqual(new Date('July 30, 2024 01:15:00'));
        expect(students.value?.[2]?.create_time).toEqual(new Date('July 21, 2024 01:15:00'));
        expect(students.value?.[2]?.courses).toEqual([]);
        expect(students.value?.[2]?.groups).toEqual([]);
        expect(students.value?.[2]?.faculties).toEqual([]);

        expect(students.value?.[3]?.username).toBe('somtin');
        expect(students.value?.[3]?.is_staff).toBe(false);
        expect(students.value?.[3]?.email).toBe('somtin.somtin@gmail.com');
        expect(students.value?.[3]?.first_name).toBe('somtin');
        expect(students.value?.[3]?.last_name).toBe('somtin');
        expect(students.value?.[3]?.last_enrolled).toBe(2023);
        expect(students.value?.[3]?.studentId).toBeNull();
        expect(students.value?.[3]?.last_login).toBeNull();
        expect(students.value?.[3]?.create_time).toEqual(new Date('July 21, 2024 01:15:00'));
        expect(students.value?.[3]?.courses).toEqual([]);
        expect(students.value?.[3]?.groups).toEqual([]);
        expect(students.value?.[3]?.faculties).toEqual([]);
    });

    it('gets students data by course', async () => {
        await getStudentsByCourse('1');
        expect(students).not.toBeNull();
        expect(Array.isArray(students.value)).toBe(true);
        expect(students.value?.length).toBe(4);

        expect(students.value?.[0]?.username).toBe('jdoe');
        expect(students.value?.[0]?.is_staff).toBe(false);
        expect(students.value?.[0]?.email).toBe('John.Doe@hotmail.com');
        expect(students.value?.[0]?.first_name).toBe('John');
        expect(students.value?.[0]?.last_name).toBe('Doe');
        expect(students.value?.[0]?.last_enrolled).toBe(2023);
        expect(students.value?.[0]?.studentId).toBeNull();
        expect(students.value?.[0]?.last_login).toBeNull();
        expect(students.value?.[0]?.create_time).toEqual(new Date('July 21, 2024 01:15:00'));
        expect(students.value?.[0]?.courses).toEqual([]);
        expect(students.value?.[0]?.groups).toEqual([]);
        expect(students.value?.[0]?.faculties).toEqual([]);

        expect(students.value?.[1]?.username).toBe('bverhae');
        expect(students.value?.[1]?.is_staff).toBe(false);
        expect(students.value?.[1]?.email).toBe('Bartje.Verhaege@gmail.com');
        expect(students.value?.[1]?.first_name).toBe('Bartje');
        expect(students.value?.[1]?.last_name).toBe('Verhaege');
        expect(students.value?.[1]?.last_enrolled).toBe(2023);
        expect(students.value?.[1]?.studentId).toBeNull();
        expect(students.value?.[1]?.last_login).toBeNull();
        expect(students.value?.[1]?.create_time).toEqual(new Date('July 21, 2024 01:15:00'));
        expect(students.value?.[1]?.courses).toEqual([]);
        expect(students.value?.[1]?.groups).toEqual([]);
        expect(students.value?.[1]?.faculties).toEqual([]);

        expect(students.value?.[2]?.username).toBe('tverslyp');
        expect(students.value?.[2]?.is_staff).toBe(true);
        expect(students.value?.[2]?.email).toBe('Tybo.Verslype@UGent.be');
        expect(students.value?.[2]?.first_name).toBe('Tybo');
        expect(students.value?.[2]?.last_name).toBe('Verslype');
        expect(students.value?.[2]?.last_enrolled).toBe(2023);
        expect(students.value?.[2]?.studentId).toBe('02012470');
        expect(students.value?.[2]?.last_login).toEqual(new Date('July 30, 2024 01:15:00'));
        expect(students.value?.[2]?.create_time).toEqual(new Date('July 21, 2024 01:15:00'));
        expect(students.value?.[2]?.courses).toEqual([]);
        expect(students.value?.[2]?.groups).toEqual([]);
        expect(students.value?.[2]?.faculties).toEqual([]);

        expect(students.value?.[3]?.username).toBe('somtin');
        expect(students.value?.[3]?.is_staff).toBe(false);
        expect(students.value?.[3]?.email).toBe('somtin.somtin@gmail.com');
        expect(students.value?.[3]?.first_name).toBe('somtin');
        expect(students.value?.[3]?.last_name).toBe('somtin');
        expect(students.value?.[3]?.last_enrolled).toBe(2023);
        expect(students.value?.[3]?.studentId).toBeNull();
        expect(students.value?.[3]?.last_login).toBeNull();
        expect(students.value?.[3]?.create_time).toEqual(new Date('July 21, 2024 01:15:00'));
        expect(students.value?.[3]?.courses).toEqual([]);
        expect(students.value?.[3]?.groups).toEqual([]);
        expect(students.value?.[3]?.faculties).toEqual([]);
    });

    it('create student', async () => {
        const exampleStudent = new Student(
            '', // id
            '', // username
            'sample.student@UGent.be', // email
            'student_first_name', // first_name
            'student_last_name', // last_name
            false, // is_staff
            2024, // last_enrolled
            new Date(), // create_time
            null, // last_login
            '', // studentId
            [],
            [],
            [],
            [],
        );

        await getStudents();
        expect(students).not.toBeNull();
        expect(Array.isArray(students.value)).toBe(true);
        const prevLength = students.value?.length ?? 0;

        await createStudent(exampleStudent);
        await getStudents();

        expect(students).not.toBeNull();
        expect(Array.isArray(students.value)).toBe(true);
        expect(students.value?.length).toBe(prevLength + 1);

        // Only check for fields that are sent to the backend
        expect(students.value?.[prevLength]?.first_name).toBe('student_first_name');
        expect(students.value?.[prevLength]?.last_name).toBe('student_last_name');
        expect(students.value?.[prevLength]?.email).toBe('sample.student@UGent.be');
    });
});

import { describe, it, expect } from 'vitest';
import { useTeacher } from '@/composables/services/teacher.service.ts';

const { teachers, teacher, getTeacherByID, getTeachersByCourse, getTeachers } = useTeacher();

function resetService(): void {
    teacher.value = null;
    teachers.value = null;
}

describe('teachers', (): void => {
    it('gets teacher data by id', async () => {
        resetService();

        await getTeacherByID('123');
        expect(teacher.value).not.toBeNull();
        expect(teacher.value?.username).toBe('tboonen');
        expect(teacher.value?.is_staff).toBe(false);
        expect(teacher.value?.email).toBe('Tom.Boonen@gmail.be');
        expect(teacher.value?.first_name).toBe('Tom');
        expect(teacher.value?.last_name).toBe('Boonen');
        expect(teacher.value?.last_enrolled).toBe(2023);
        expect(teacher.value?.last_login).toBeNull();
        expect(teacher.value?.create_time).toEqual(new Date('July 21, 2024 01:15:00'));
        expect(teacher.value?.courses).toEqual([]);
        expect(teacher.value?.faculties).toEqual([]);
    });

    it('gets teacher data', async () => {
        resetService();

        await getTeachers();
        expect(teachers).not.toBeNull();
        expect(Array.isArray(teachers.value)).toBe(true);
        expect(teachers.value?.length).toBe(2);

        expect(teachers.value?.[0]?.username).toBe('tboonen');
        expect(teachers.value?.[0]?.is_staff).toBe(false);
        expect(teachers.value?.[0]?.email).toBe('Tom.Boonen@gmail.be');
        expect(teachers.value?.[0]?.first_name).toBe('Tom');
        expect(teachers.value?.[0]?.last_name).toBe('Boonen');
        expect(teachers.value?.[0]?.last_enrolled).toBe(2023);
        expect(teachers.value?.[0]?.last_login).toBeNull();
        expect(teachers.value?.[0]?.create_time).toEqual(new Date('July 21, 2024 01:15:00'));
        expect(teachers.value?.[0]?.courses).toEqual([]);
        expect(teachers.value?.[0]?.faculties).toEqual([]);

        expect(teachers.value?.[1]?.username).toBe('psagan');
        expect(teachers.value?.[1]?.is_staff).toBe(false);
        expect(teachers.value?.[1]?.email).toBe('Peter.Sagan@gmail.com');
        expect(teachers.value?.[1]?.first_name).toBe('Peter');
        expect(teachers.value?.[1]?.last_name).toBe('Sagan');
        expect(teachers.value?.[1]?.last_enrolled).toBe(2023);
        expect(teachers.value?.[0]?.last_login).toBeNull();
        expect(teachers.value?.[0]?.create_time).toEqual(new Date('July 21, 2024 01:15:00'));
        expect(teachers.value?.[1]?.courses).toEqual([]);
        expect(teachers.value?.[1]?.faculties).toEqual([]);
    });

    it('gets teacher data by course', async () => {
        resetService();

        await getTeachersByCourse('1');
        expect(teachers).not.toBeNull();
        expect(Array.isArray(teachers.value)).toBe(true);
        expect(teachers.value?.length).toBe(2);

        expect(teachers.value?.[0]?.username).toBe('tboonen');
        expect(teachers.value?.[0]?.is_staff).toBe(false);
        expect(teachers.value?.[0]?.email).toBe('Tom.Boonen@gmail.be');
        expect(teachers.value?.[0]?.first_name).toBe('Tom');
        expect(teachers.value?.[0]?.last_name).toBe('Boonen');
        expect(teachers.value?.[0]?.last_enrolled).toBe(2023);
        expect(teachers.value?.[0]?.last_login).toBeNull();
        expect(teachers.value?.[0]?.create_time).toEqual(new Date('July 21, 2024 01:15:00'));
        expect(teachers.value?.[0]?.courses).toEqual([]);
        expect(teachers.value?.[0]?.faculties).toEqual([]);

        expect(teachers.value?.[1]?.username).toBe('psagan');
        expect(teachers.value?.[1]?.is_staff).toBe(false);
        expect(teachers.value?.[1]?.email).toBe('Peter.Sagan@gmail.com');
        expect(teachers.value?.[1]?.first_name).toBe('Peter');
        expect(teachers.value?.[1]?.last_name).toBe('Sagan');
        expect(teachers.value?.[1]?.last_enrolled).toBe(2023);
        expect(teachers.value?.[0]?.last_login).toBeNull();
        expect(teachers.value?.[0]?.create_time).toEqual(new Date('July 21, 2024 01:15:00'));
        expect(teachers.value?.[1]?.courses).toEqual([]);
        expect(teachers.value?.[1]?.faculties).toEqual([]);
    });
});

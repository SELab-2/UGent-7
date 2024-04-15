import { describe, it, expect } from 'vitest';

import { Course, getAcademicYear, getAcademicYears } from '@/types/Course';
import { courseData } from './data';
import { createCourse } from './helper';

describe('course type', () => {
    it('create instance of course with correct properties', () => {
        const course = createCourse(courseData);

        expect(course).toBeInstanceOf(Course);
        expect(course.id).toBe(courseData.id);
        expect(course.name).toBe(courseData.name);
        expect(course.excerpt).toBe(courseData.excerpt);
        expect(course.description).toBe(courseData.description);
        expect(course.academic_startyear).toBe(courseData.academic_startyear);
        expect(course.parent_course).toBe(courseData.parent_course);
        expect(course.faculty).toBe(courseData.faculty);
        expect(course.teachers).toStrictEqual(courseData.teachers);
        expect(course.assistants).toStrictEqual(courseData.assistants);
        expect(course.students).toStrictEqual(courseData.students);
        expect(course.projects).toStrictEqual(courseData.projects);
    });

    it('create a course instance from JSON data', () => {
        const courseJSON = { ...courseData };
        const course = Course.fromJSON(courseJSON as any);

        expect(course).toBeInstanceOf(Course);
        expect(course.id).toBe(courseData.id);
        expect(course.name).toBe(courseData.name);
        expect(course.description).toBe(courseData.description);
        expect(course.academic_startyear).toBe(courseData.academic_startyear);
        expect(course.parent_course).toBe(courseData.parent_course);
        expect(course.faculty).toBe(courseData.faculty);
        expect(course.teachers).toStrictEqual(courseData.teachers);
        expect(course.assistants).toStrictEqual(courseData.assistants);
        expect(course.students).toStrictEqual(courseData.students);
        expect(course.projects).toStrictEqual(courseData.projects);
    });

    it('getCourseYear method', () => {
        const course = createCourse(courseData);

        expect(course.getCourseYear()).toBe(`${courseData.academic_startyear} - ${courseData.academic_startyear + 1}`);
    });

    it('getAcademicYear method', () => {
        expect(getAcademicYear(new Date('November 1, 2024 04:20:00'))).toBe(2024);
        expect(getAcademicYear(new Date('February 1, 2024 04:20:00'))).toBe(2023);
    });

    it('getAcademicYears method', () => {
        expect(getAcademicYears(2024, 2024)).toStrictEqual([2024]);
        expect(getAcademicYears(2024, 2025)).toStrictEqual([2025, 2024]);
        expect(getAcademicYears(2024, 2026)).toStrictEqual([2026, 2025, 2024]);
    });
});

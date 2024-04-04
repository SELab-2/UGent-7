/* eslint-disable @typescript-eslint/no-unused-vars */
import { describe, it, expect } from 'vitest';
import { Course } from '@/types/Course.ts';

import { useCourses } from '@/composables/services/courses.service.ts';

const {
    courses,
    course,

    getCourseByID,
    getCourses,
    getCoursesByStudent,

} = useCourses();

// "describe" bundles tests about 1 specific thing; here we're testing course
// aka a test suite
describe('course', (): void => {
    // "it" is used to specify tests
    // you can also import "test" instead of "it", because it's the exact same
    // but with "it", it's easy to read => it (referring to the course) returns correct course year
    it('returns correct course year', (): void => {
        const course: Course = new Course('1', 'course', 'description', 2003);
        // use expect for assertions
        // after expect, there are a multitude of possible functions such as:
        // toBe, toEqual, toContain
        // check https://vitest.dev/api/expect.html for all possibilities
        expect(course.getCourseYear()).toBe('2003 - 2004');
        // assert can also be used instead, if you like its syntax more
        // check out https://vitest.dev/api/assert.html for more info
    });

    it('gets course data by id', async () => {
        await getCourseByID('1');
        expect(course.value).not.toBeNull();
        expect(course.value?.name).toBe('Math');
        expect(course.value?.parent_course).toBeNull();
        expect(course.value?.academic_startyear).toBe(2023);
        expect(course.value?.description).toBe('Math course');
        expect(course.value?.students).toEqual([]);
        expect(course.value?.teachers).toEqual([]);
        expect(course.value?.assistants).toEqual([]);
        expect(course.value?.projects).toEqual([]);
    });

    it('gets courses data', async () => {
        await getCourses();
        expect(courses.value).not.toBeNull();
        expect(courses.value?.[0]?.name).toBe('Math');
        expect(courses.value?.[0]?.parent_course).toBeNull();
        expect(courses.value?.[0]?.academic_startyear).toBe(2023);
        expect(courses.value?.[0]?.description).toBe('Math course');
        expect(courses.value?.[0]?.students).toEqual([]);
        expect(courses.value?.[0]?.teachers).toEqual([]);
        expect(courses.value?.[0]?.assistants).toEqual([]);
        expect(courses.value?.[0]?.projects).toEqual([]);

        expect(courses.value?.[1]?.name).toBe('Sel2');
        expect(courses.value?.[1]?.parent_course).toBe('3');
        expect(courses.value?.[1]?.academic_startyear).toBe(2023);
        expect(courses.value?.[1]?.description).toBe('Software course');
        expect(courses.value?.[1]?.students).toEqual([]);
        expect(courses.value?.[1]?.teachers).toEqual([]);
        expect(courses.value?.[1]?.assistants).toEqual([]);
        expect(courses.value?.[1]?.projects).toEqual([]);

        expect(courses.value?.[2]?.name).toBe('Sel1');
        expect(courses.value?.[2]?.parent_course).toBeNull();
        expect(courses.value?.[2]?.academic_startyear).toBe(2022);
        expect(courses.value?.[2]?.description).toBe('Software course');
        expect(courses.value?.[2]?.students).toEqual([]);
        expect(courses.value?.[2]?.teachers).toEqual([]);
        expect(courses.value?.[2]?.assistants).toEqual([]);
        expect(courses.value?.[2]?.projects).toEqual([]);

        expect(courses.value?.[3]?.name).toBe('Math');
        expect(courses.value?.[3]?.parent_course).toBe('1');
        expect(courses.value?.[3]?.academic_startyear).toBe(2024);
        expect(courses.value?.[3]?.description).toBe('Math course');
        expect(courses.value?.[3]?.students).toEqual([]);
        expect(courses.value?.[3]?.teachers).toEqual([]);
        expect(courses.value?.[3]?.assistants).toEqual([]);
        expect(courses.value?.[3]?.projects).toEqual([]);

        expect(courses.value?.[4]?.name).toBe('Math');
        expect(courses.value?.[4]?.parent_course).toBe('12');
        expect(courses.value?.[4]?.academic_startyear).toBe(2025);
        expect(courses.value?.[4]?.description).toBe('Math course');
        expect(courses.value?.[4]?.students).toEqual([]);
        expect(courses.value?.[4]?.teachers).toEqual([]);
        expect(courses.value?.[4]?.assistants).toEqual([]);
        expect(courses.value?.[4]?.projects).toEqual([]);

        expect(courses.value?.[5]?.name).toBe('Club brugge');
        expect(courses.value?.[5]?.parent_course).toBeNull();
        expect(courses.value?.[5]?.academic_startyear).toBe(2023);
        expect(courses.value?.[5]?.description).toBeNull();
        expect(courses.value?.[5]?.students).toEqual([]);
        expect(courses.value?.[5]?.teachers).toEqual([]);
        expect(courses.value?.[5]?.assistants).toEqual([]);
        expect(courses.value?.[5]?.projects).toEqual([]);

        expect(courses.value?.[6]?.name).toBe('vergeet barbara');
        expect(courses.value?.[6]?.parent_course).toBeNull();
        expect(courses.value?.[6]?.academic_startyear).toBe(2023);
        expect(courses.value?.[6]?.description).toBeNull();
        expect(courses.value?.[6]?.students).toEqual([]);
        expect(courses.value?.[6]?.teachers).toEqual([]);
        expect(courses.value?.[6]?.assistants).toEqual([]);
        expect(courses.value?.[6]?.projects).toEqual([]);
    });

    it('gets courses data by student', async () => {
        await getCoursesByStudent('1');
        expect(courses).not.toBeNull();
        expect(Array.isArray(courses.value)).toBe(true);
        expect(courses.value?.length).toBe(3);

        expect(courses.value?.[0]?.name).toBe('Math');
        expect(courses.value?.[0]?.parent_course).toBeNull();
        expect(courses.value?.[0]?.academic_startyear).toBe(2023);
        expect(courses.value?.[0]?.description).toBe('Math course');
        expect(courses.value?.[0]?.students).toEqual([]);
        expect(courses.value?.[0]?.teachers).toEqual([]);
        expect(courses.value?.[0]?.assistants).toEqual([]);
        expect(courses.value?.[0]?.projects).toEqual([]);

        expect(courses.value?.[1]?.name).toBe('Sel2');
        expect(courses.value?.[1]?.parent_course).toBe('3');
        expect(courses.value?.[1]?.academic_startyear).toBe(2023);
        expect(courses.value?.[1]?.description).toBe('Software course');
        expect(courses.value?.[1]?.students).toEqual([]);
        expect(courses.value?.[1]?.teachers).toEqual([]);
        expect(courses.value?.[1]?.assistants).toEqual([]);
        expect(courses.value?.[1]?.projects).toEqual([]);

        expect(courses.value?.[2]?.name).toBe('Sel1');
        expect(courses.value?.[2]?.parent_course).toBeNull();
        expect(courses.value?.[2]?.academic_startyear).toBe(2022);
        expect(courses.value?.[2]?.description).toBe('Software course');
        expect(courses.value?.[2]?.students).toEqual([]);
        expect(courses.value?.[2]?.teachers).toEqual([]);
        expect(courses.value?.[2]?.assistants).toEqual([]);
        expect(courses.value?.[2]?.projects).toEqual([]);
    });
});

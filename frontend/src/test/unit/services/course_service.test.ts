/* eslint-disable @typescript-eslint/no-unused-vars */
import { describe, it } from 'vitest';
// import { Course } from '@/types/Course.ts';
//
// import { useCourses } from '@/composables/services/course.service.ts';
//
// const {
//     pagination,
//     courses,
//     course,
//
//     getCourseByID,
//     searchCourses,
//     getCourses,
//     getCoursesByStudent,
//     getCoursesByTeacher,
//     getCourseByAssistant,
//
//     createCourse,
//     cloneCourse,
//     deleteCourse,
// } = useCourses();

// function resetService(): void {
//     course.value = null;
//     courses.value = null;
// }

describe('course', (): void => {
    it('aaaa');
    // it('gets course data by id', async () => {
    //     resetService();
    //
    //     await getCourseByID('1');
    //     expect(course.value).not.toBeNull();
    //     expect(course.value?.name).toBe('Math');
    //     expect(course.value?.parent_course).toBeNull();
    //     expect(course.value?.academic_startyear).toBe(2023);
    //     expect(course.value?.description).toBe('Math course');
    //     expect(course.value?.students).toBeNull();
    //     expect(course.value?.teachers).toBeNull();
    //     expect(course.value?.assistants).toBeNull();
    //     expect(course.value?.projects).toBeNull();
    // });
    //
    // it('gets courses data', async () => {
    //     resetService();
    //
    //     await getCourses();
    //     expect(courses.value).not.toBeNull();
    //     expect(courses.value?.[0]?.name).toBe('Math');
    //     expect(courses.value?.[0]?.parent_course).toBeNull();
    //     expect(courses.value?.[0]?.academic_startyear).toBe(2023);
    //     expect(courses.value?.[0]?.description).toBe('Math course');
    //     expect(courses.value?.[0]?.students).toBeNull();
    //     expect(courses.value?.[0]?.teachers).toBeNull();
    //     expect(courses.value?.[0]?.assistants).toBeNull();
    //     expect(courses.value?.[0]?.projects).toBeNull();
    //
    //     expect(courses.value?.[1]?.name).toBe('Sel2');
    //     expect(courses.value?.[1]?.parent_course).toBe('3');
    //     expect(courses.value?.[1]?.academic_startyear).toBe(2023);
    //     expect(courses.value?.[1]?.description).toBe('Software course');
    //     expect(courses.value?.[1]?.students).toBeNull();
    //     expect(courses.value?.[1]?.teachers).toBeNull();
    //     expect(courses.value?.[1]?.assistants).toBeNull();
    //     expect(courses.value?.[1]?.projects).toBeNull();
    //
    //     expect(courses.value?.[2]?.name).toBe('Sel1');
    //     expect(courses.value?.[2]?.parent_course).toBeNull();
    //     expect(courses.value?.[2]?.academic_startyear).toBe(2022);
    //     expect(courses.value?.[2]?.description).toBe('Software course');
    //     expect(courses.value?.[2]?.students).toBeNull();
    //     expect(courses.value?.[2]?.teachers).toBeNull();
    //     expect(courses.value?.[2]?.assistants).toBeNull();
    //     expect(courses.value?.[2]?.projects).toBeNull();
    //
    //     expect(courses.value?.[3]?.name).toBe('Math');
    //     expect(courses.value?.[3]?.parent_course).toBe('1');
    //     expect(courses.value?.[3]?.academic_startyear).toBe(2024);
    //     expect(courses.value?.[3]?.description).toBe('Math course');
    //     expect(courses.value?.[3]?.students).toBeNull();
    //     expect(courses.value?.[3]?.teachers).toBeNull();
    //     expect(courses.value?.[3]?.assistants).toBeNull();
    //     expect(courses.value?.[3]?.projects).toBeNull();
    //
    //     expect(courses.value?.[4]?.name).toBe('Math');
    //     expect(courses.value?.[4]?.parent_course).toBe('12');
    //     expect(courses.value?.[4]?.academic_startyear).toBe(2025);
    //     expect(courses.value?.[4]?.description).toBe('Math course');
    //     expect(courses.value?.[4]?.students).toBeNull();
    //     expect(courses.value?.[4]?.teachers).toBeNull();
    //     expect(courses.value?.[4]?.assistants).toBeNull();
    //     expect(courses.value?.[4]?.projects).toBeNull();
    //
    //     expect(courses.value?.[5]?.name).toBe('Club brugge');
    //     expect(courses.value?.[5]?.parent_course).toBeNull();
    //     expect(courses.value?.[5]?.academic_startyear).toBe(2023);
    //     expect(courses.value?.[5]?.description).toBeNull();
    //     expect(courses.value?.[5]?.students).toBeNull();
    //     expect(courses.value?.[5]?.teachers).toBeNull();
    //     expect(courses.value?.[5]?.assistants).toBeNull();
    //     expect(courses.value?.[5]?.projects).toBeNull();
    //
    //     expect(courses.value?.[6]?.name).toBe('vergeet barbara');
    //     expect(courses.value?.[6]?.parent_course).toBeNull();
    //     expect(courses.value?.[6]?.academic_startyear).toBe(2023);
    //     expect(courses.value?.[6]?.description).toBeNull();
    //     expect(courses.value?.[6]?.students).toBeNull();
    //     expect(courses.value?.[6]?.teachers).toBeNull();
    //     expect(courses.value?.[6]?.assistants).toBeNull();
    //     expect(courses.value?.[6]?.projects).toBeNull();
    // });
    //
    // it('gets courses data by student', async () => {
    //     resetService();
    //
    //     await getCoursesByStudent('1');
    //     expect(courses).not.toBeNull();
    //     expect(Array.isArray(courses.value)).toBe(true);
    //     expect(courses.value?.length).toBe(3);
    //
    //     expect(courses.value?.[0]?.name).toBe('Math');
    //     expect(courses.value?.[0]?.parent_course).toBeNull();
    //     expect(courses.value?.[0]?.academic_startyear).toBe(2023);
    //     expect(courses.value?.[0]?.description).toBe('Math course');
    //     expect(courses.value?.[0]?.students).toBeNull();
    //     expect(courses.value?.[0]?.teachers).toBeNull();
    //     expect(courses.value?.[0]?.assistants).toBeNull();
    //     expect(courses.value?.[0]?.projects).toBeNull();
    //
    //     expect(courses.value?.[1]?.name).toBe('Sel2');
    //     expect(courses.value?.[1]?.parent_course).toBe('3');
    //     expect(courses.value?.[1]?.academic_startyear).toBe(2023);
    //     expect(courses.value?.[1]?.description).toBe('Software course');
    //     expect(courses.value?.[1]?.students).toBeNull();
    //     expect(courses.value?.[1]?.teachers).toBeNull();
    //     expect(courses.value?.[1]?.assistants).toBeNull();
    //     expect(courses.value?.[1]?.projects).toBeNull();
    //
    //     expect(courses.value?.[2]?.name).toBe('Sel1');
    //     expect(courses.value?.[2]?.parent_course).toBeNull();
    //     expect(courses.value?.[2]?.academic_startyear).toBe(2022);
    //     expect(courses.value?.[2]?.description).toBe('Software course');
    //     expect(courses.value?.[2]?.students).toBeNull();
    //     expect(courses.value?.[2]?.teachers).toBeNull();
    //     expect(courses.value?.[2]?.assistants).toBeNull();
    //     expect(courses.value?.[2]?.projects).toBeNull();
    // });
    //
    // it('create course', async () => {
    //     resetService();
    //
    //     const exampleCourse = new Course(
    //         'course_id', // id
    //         'course_name', // name
    //         'course_excerpt', // excerpt
    //         'course_description', // description
    //         2024, // acedemic_startyear,
    //         null, // parent_course
    //         null, // faculty
    //         [], // teachers
    //         [], // assistants
    //         [], // students
    //         [], // projects
    //     );
    //
    //     await getCourses();
    //     expect(courses).not.toBeNull();
    //     expect(Array.isArray(courses.value)).toBe(true);
    //     const prevLength = courses.value?.length ?? 0;
    //
    //     await createCourse(exampleCourse);
    //     await getCourses();
    //
    //     expect(courses).not.toBeNull();
    //     expect(Array.isArray(courses.value)).toBe(true);
    //     expect(courses.value?.length).toBe(prevLength + 1);
    //
    //     // Only check for fields that are sent to the backend
    //     expect(courses.value?.[prevLength]?.id).toBe('course_id');
    //     expect(courses.value?.[prevLength]?.name).toBe('course_name');
    //     expect(courses.value?.[prevLength]?.description).toBe('course_description');
    //     expect(courses.value?.[prevLength]?.excerpt).toBe('course_excerpt');
    //     expect(courses.value?.[prevLength]?.academic_startyear).toBe(2024);
    // });
});

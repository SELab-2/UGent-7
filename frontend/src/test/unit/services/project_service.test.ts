/* eslint-disable @typescript-eslint/no-unused-vars */
import { describe, it, expect, assertType } from 'vitest';
import { useProject } from '@/composables/services/project.service.ts';
import { useCourses } from '@/composables/services/course.service';
import { Project } from '@/types/Project';
import { type Course } from '@/types/Course';
import { SubmissionStatus } from '@/types/SubmisionStatus';
import { type Group } from '@/types/Group';

const {
    projects,
    project,
    getProjectByID,
    getProjectsByCourse,
    getProjectsByCourseAndDeadline,
    getProjectsByStudent,

    createProject,
    deleteProject,
} = useProject();

const { course, getCourseByID } = useCourses();

function resetService(): void {
    project.value = null;
    projects.value = null;
}

describe('project', (): void => {
    it('gets project data by id', async () => {
        resetService();

        await getProjectByID('0');
        expect(project.value).not.toBeNull();
        expect(project.value?.name).toBe('project0');
        expect(project.value?.description).toBe('project0 description');
        expect(project.value?.visible).toBe(true);
        expect(project.value?.archived).toBe(false);
        expect(project.value?.locked_groups).toBe(false);
        expect(project.value?.start_date).toStrictEqual(new Date('November 11, 2024 01:15:00'));
        expect(project.value?.deadline).toStrictEqual(new Date('November 11, 2025 01:15:00'));
        expect(project.value?.max_score).toBe(100);
        expect(project.value?.score_visible).toBe(true);
        expect(project.value?.group_size).toBe(5);
        assertType(project.value?.course!);
        assertType(project.value?.status!);
        assertType(project.value?.structure_file!);
        expect(project.value?.structureChecks).toBe(null);
        expect(project.value?.extra_checks).toBe(null);
        assertType(Array.isArray(project.value?.groups));
        assertType((project.value?.groups?.[0] ?? null)!);
        expect(project.value?.submissions).toBe(null);
    });

    it('gets projects data by course', async () => {
        resetService();

        await getProjectsByCourse('1');
        expect(projects.value).not.toBeNull();
        expect(Array.isArray(projects.value)).toBe(true);
        expect(projects.value?.length).toBe(2);

        expect(projects.value?.[0]?.name).toBe('project0');
        expect(projects.value?.[0]?.description).toBe('project0 description');
        expect(projects.value?.[0]?.visible).toBe(true);
        expect(projects.value?.[0]?.archived).toBe(false);
        expect(projects.value?.[0]?.locked_groups).toBe(false);
        expect(projects.value?.[0]?.start_date).toStrictEqual(new Date('November 11, 2024 01:15:00'));
        expect(projects.value?.[0]?.deadline).toStrictEqual(new Date('November 11, 2025 01:15:00'));
        expect(projects.value?.[0]?.max_score).toBe(100);
        expect(projects.value?.[0]?.score_visible).toBe(true);
        expect(projects.value?.[0]?.group_size).toBe(5);
        assertType(projects.value?.[0]?.course!);
        assertType(projects.value?.[0]?.status!);
        assertType(projects.value?.[0]?.structure_file!);
        expect(projects.value?.[0]?.structureChecks).toBe(null);
        expect(projects.value?.[0]?.extra_checks).toBe(null);
        assertType(Array.isArray(projects.value?.[0]?.groups));
        assertType((projects.value?.[0]?.groups?.[0] ?? null)!);
        expect(projects.value?.[0]?.submissions).toBe(null);

        expect(projects.value?.[1]?.name).toBe('project1');
        expect(projects.value?.[1]?.description).toBe('project1 description');
        expect(projects.value?.[1]?.visible).toBe(true);
        expect(projects.value?.[1]?.archived).toBe(false);
        expect(projects.value?.[1]?.locked_groups).toBe(false);
        expect(projects.value?.[1]?.start_date).toStrictEqual(new Date('December 11, 2024 01:15:00'));
        expect(projects.value?.[1]?.deadline).toStrictEqual(new Date('December 11, 2025 01:15:00'));
        expect(projects.value?.[1]?.max_score).toBe(50);
        expect(projects.value?.[1]?.score_visible).toBe(false);
        expect(projects.value?.[1]?.group_size).toBe(8);
        assertType(projects.value?.[1]?.course!);
        assertType(projects.value?.[1]?.status!);
        assertType(projects.value?.[1]?.structure_file!);
        expect(projects.value?.[1]?.structureChecks).toBe(null);
        expect(projects.value?.[1]?.extra_checks).toBe(null);
        assertType(Array.isArray(projects.value?.[1]?.groups));
        assertType((projects.value?.[0]?.groups?.[1] ?? null)!);
        expect(projects.value?.[1]?.submissions).toBe(null);
    });

    it('gets projects data by student', async () => {
        resetService();

        await getProjectsByStudent('1');
        expect(projects).not.toBeNull();
        expect(Array.isArray(projects.value)).toBe(true);
        expect(projects.value?.length).toBe(2);
        expect(projects.value).not.toBeNull();

        expect(projects.value?.[0]?.name).toBe('project0');
        expect(projects.value?.[0]?.description).toBe('project0 description');
        expect(projects.value?.[0]?.visible).toBe(true);
        expect(projects.value?.[0]?.archived).toBe(false);
        expect(projects.value?.[0]?.locked_groups).toBe(false);
        expect(projects.value?.[0]?.start_date).toStrictEqual(new Date('November 11, 2024 01:15:00'));
        expect(projects.value?.[0]?.deadline).toStrictEqual(new Date('November 11, 2025 01:15:00'));
        expect(projects.value?.[0]?.max_score).toBe(100);
        expect(projects.value?.[0]?.score_visible).toBe(true);
        expect(projects.value?.[0]?.group_size).toBe(5);
        assertType(projects.value?.[0]?.course!);
        assertType(projects.value?.[0]?.status!);
        assertType(projects.value?.[0]?.structure_file!);
        expect(projects.value?.[0]?.structureChecks).toBe(null);
        expect(projects.value?.[0]?.extra_checks).toBe(null);
        assertType(Array.isArray(projects.value?.[0]?.groups));
        assertType((projects.value?.[0]?.groups?.[0] ?? null)!);
        expect(projects.value?.[0]?.submissions).toBe(null);

        expect(projects.value?.[1]?.name).toBe('project1');
        expect(projects.value?.[1]?.description).toBe('project1 description');
        expect(projects.value?.[1]?.visible).toBe(true);
        expect(projects.value?.[1]?.archived).toBe(false);
        expect(projects.value?.[1]?.locked_groups).toBe(false);
        expect(projects.value?.[1]?.start_date).toStrictEqual(new Date('December 11, 2024 01:15:00'));
        expect(projects.value?.[1]?.deadline).toStrictEqual(new Date('December 11, 2025 01:15:00'));
        expect(projects.value?.[1]?.max_score).toBe(50);
        expect(projects.value?.[1]?.score_visible).toBe(false);
        expect(projects.value?.[1]?.group_size).toBe(8);
        assertType(projects.value?.[1]?.course!);
        assertType(projects.value?.[1]?.status!);
        assertType(projects.value?.[1]?.structure_file!);
        expect(projects.value?.[1]?.structureChecks).toBe(null);
        expect(projects.value?.[1]?.extra_checks).toBe(null);
        assertType(Array.isArray(projects.value?.[1]?.groups));
        assertType((projects.value?.[0]?.groups?.[1] ?? null)!);
        expect(projects.value?.[1]?.submissions).toBe(null);
    });

    it('create project', async () => {
        resetService();

        const courseId = '1';
        await getCourseByID(courseId);

        const exampleProject = new Project(
            '', // id
            'project_name', // name
            'project_description', // description
            true, // visible
            false, // archived
            false, // locked_groups
            new Date('November 1, 2024 04:20:00'), // start_data
            new Date('November 2, 2024 04:20:00'), // deadline
            20, // max_score
            false, // score_visible
            5, // group_size
            course.value!, // course
            new SubmissionStatus(0, 0, 0, 0), // submission_status
            null, // structureChecks
            null, // extra_checks
            null, // groups
            null, // submissions
        );

        await getProjectsByCourse(courseId);

        expect(projects).not.toBeNull();
        expect(Array.isArray(projects.value)).toBe(true);
        const prevLength = projects.value?.length ?? 0;

        // await createProject(exampleProject, courseId, 0);
        // await getProjectsByCourse(courseId);

        // expect(projects).not.toBeNull();
        // expect(Array.isArray(projects.value)).toBe(true);
        // expect(projects.value?.length).toBe(prevLength + 1);

        // // Only check for fields that are sent to the backend
        // expect(projects.value?.[prevLength]?.name).toBe('project_name');
        // expect(projects.value?.[prevLength]?.description).toBe('project_description');
        // expect(projects.value?.[prevLength]?.visible).toBe(true);
        // expect(projects.value?.[prevLength]?.archived).toBe(false);
        // expect(projects.value?.[prevLength]?.locked_groups).toBe(false);
        // expect(projects.value?.[prevLength]?.start_date).toStrictEqual(new Date('November 1, 2024 04:20:00'));
        // expect(projects.value?.[prevLength]?.deadline).toStrictEqual(new Date('November 2, 2024 04:20:00'));
        // expect(projects.value?.[prevLength]?.max_score).toBe(20);
        // expect(projects.value?.[prevLength]?.score_visible).toBe(false);
        // expect(projects.value?.[prevLength]?.group_size).toBe(5);
        // expect(projects.value?.[prevLength]?.structure_file).toBe(null);
        // expect(projects.value?.[prevLength]?.course).toBe(null);
    });
});

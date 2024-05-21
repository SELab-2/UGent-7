/* eslint-disable @typescript-eslint/no-unused-vars */

/* eslint-disable @typescript-eslint/no-unused-vars */
import { describe, it, expect, assertType } from 'vitest';
import { useGroup } from '@/composables/services/group.service.ts';
import { Group } from '@/types/Group';
import { useProject } from '@/composables/services/project.service';
import { type Project } from '@/types/Project';

const {
    groups,
    group,
    getGroupByID,
    getGroupsByProject,
    getGroupsByStudent,

    createGroup,
    deleteGroup,
} = useGroup();

function resetService(): void {
    group.value = null;
    groups.value = null;
}

const { project, getProjectByID } = useProject();

describe('group', (): void => {
    it('gets group data by id', async () => {
        resetService();

        await getGroupByID('0');
        expect(group.value).not.toBeNull();
        expect(group.value?.id).toBe('0');
        expect(group.value?.score).toBe(20);
        assertType(group.value?.project as Project);
        expect(group.value?.students).toBeNull();
        expect(group.value?.submissions).toBeNull();
    });

    it('gets groups data by project', async () => {
        resetService();

        await getGroupsByProject('3');
        expect(groups).not.toBeNull();
        expect(Array.isArray(groups.value)).toBe(true);
        expect(groups.value?.length).toBe(2);

        expect(groups.value?.[0].id).toBe('0');
        expect(groups.value?.[0].score).toBe(20);
        assertType(groups.value?.[0].project as Project)
        expect(groups.value?.[0].students).toBeNull;
        expect(groups.value?.[0].submissions).toBeNull();

        expect(groups.value?.[1].id).toBe('1');
        expect(groups.value?.[1].score).toBe(18);
        assertType(groups.value?.[1].project as Project)
        expect(groups.value?.[1].students).toBeNull;
        expect(groups.value?.[1].submissions).toBeNull();
    });

    it('gets groups data by student', async () => {
        resetService();

        await getGroupsByStudent('1');
        expect(groups.value).not.toBeNull();
        expect(Array.isArray(groups.value)).toBe(true);
        expect(groups.value?.length).toBe(1);

        expect(groups.value?.[0].id).toBe('0');
        expect(groups.value?.[0].score).toBe(20);
        assertType(groups.value?.[0].project as Project)
        expect(groups.value?.[0].students).toBeNull;
        expect(groups.value?.[0].submissions).toBeNull();
    });

    // it('create group', async () => {
    //     resetService();

    //     const projectId = '0';
    //     await getProjectByID(projectId);
    //     const exampleProject: Project | null = project.value;
    //     expect(exampleProject).not.toBeNull();

    //     const exampleGroup = new Group(
    //         '', // id
    //         10, // score
    //         exampleProject, // project
    //         [], // students
    //         [], // submissions
    //     );

    //     await getGroupsByProject(projectId);

    //     expect(groups).not.toBeNull();
    //     expect(Array.isArray(groups.value)).toBe(true);
    //     const prevLength = groups.value?.length ?? 0;

    //     await createGroup(exampleGroup, projectId);
    //     await getGroupsByProject(projectId);

    //     expect(groups).not.toBeNull();
    //     expect(Array.isArray(groups.value)).toBe(true);
    //     expect(groups.value?.length).toBe(prevLength + 1);

    //     // Only check for fields that are sent to the backend
    //     expect(groups.value?.[prevLength]?.score).toBe(10);
    //     expect(groups.value?.[prevLength]?.project).toBeNull();
    // });
});

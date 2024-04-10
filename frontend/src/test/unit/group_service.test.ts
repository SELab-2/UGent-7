/* eslint-disable @typescript-eslint/no-unused-vars */
import { describe, it, expect } from 'vitest';
import { useGroup } from '@/composables/services/groups.service.ts';
import { Group } from '@/types/Group';
import { useProject } from '@/composables/services/project.service';
import { type Project } from '@/types/Projects';

const { groups, group, getGroupByID, getGroupsByProject, getGroupsByStudent, createGroup } = useGroup();
const { project, getProjectByID } = useProject();

describe('group', (): void => {
    it('gets group data by id', async () => {
        await getGroupByID('0');
        expect(group.value).not.toBeNull();
        expect(group.value?.score).toBe(20);
        expect(group.value?.id).toBe('0');
        expect(group.value?.project).toBeNull();
        expect(group.value?.students).toEqual([]);
        expect(group.value?.submissions).toEqual([]);
    });

    it('gets groups data by project', async () => {
        await getGroupsByProject('0');
        // console.log(groups.value)
        // Ensure group data is not null
        expect(groups.value).not.toBeNull();
        expect(Array.isArray(groups.value)).toBe(true);
        expect(groups.value?.length).toBe(2);

        expect(groups.value?.[0]).not.toBeNull();
        expect(groups.value?.[0]?.score).toBe(20);
        expect(groups.value?.[0]?.id).toBe('0');
        expect(groups.value?.[0]?.project).toBeNull();
        expect(groups.value?.[0]?.students).toEqual([]);
        expect(groups.value?.[0]?.submissions).toEqual([]);

        expect(groups.value?.[1]).not.toBeNull();
        expect(groups.value?.[1]?.score).toBe(18);
        expect(groups.value?.[1]?.id).toBe('1');
        expect(groups.value?.[1]?.project).toBeNull();
        expect(groups.value?.[1]?.students).toEqual([]);
        expect(groups.value?.[1]?.submissions).toEqual([]);
    });

    it('gets groups data by student', async () => {
        await getGroupsByStudent('1');
        expect(groups.value).not.toBeNull();
        expect(Array.isArray(groups.value)).toBe(true);
        expect(groups.value?.length).toBe(1);

        expect(groups.value?.[0]).not.toBeNull();
        expect(groups.value?.[0]?.score).toBe(20);
        expect(groups.value?.[0]?.id).toBe('0');
        expect(groups.value?.[0]?.project).toBeNull();
        expect(groups.value?.[0]?.students).toEqual([]);
        expect(groups.value?.[0]?.submissions).toEqual([]);
    });

    it('create group', async () => {
        await getProjectByID('0');
        const exampleProject: Project = project.value!;

        const exampleGroup = new Group(
            '', // id
            10, // score
            exampleProject, // project
            [], // students
            [], // submissions
        );

        await getGroupsByProject('0');

        expect(groups).not.toBeNull();
        expect(Array.isArray(groups.value)).toBe(true);
        const prevLength = groups.value?.length ?? 0;

        await createGroup(exampleGroup, '0');
        await getGroupsByProject('0');

        expect(groups).not.toBeNull();
        expect(Array.isArray(groups.value)).toBe(true);
        expect(groups.value?.length).toBe(prevLength + 1);

        expect(groups.value?.[prevLength]?.score).toBe(10);
        expect(groups.value?.[prevLength]?.project).toBeNull();
    });
});

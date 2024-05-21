/* eslint-disable @typescript-eslint/no-non-null-assertion */
/* eslint-disable @typescript-eslint/no-unused-expressions */
/* eslint-disable @typescript-eslint/no-non-null-asserted-optional-chain */

import { describe, it, expect, assertType } from 'vitest';
import { useGroup } from '@/composables/services/group.service.ts';
import { type Project } from '@/types/Project';

const { groups, group, getGroupByID, getGroupsByProject, getGroupsByStudent } = useGroup();

function resetService(): void {
    group.value = null;
    groups.value = null;
}

describe('group', (): void => {
    it('gets group data by id', async () => {
        resetService();

        await getGroupByID('0');
        expect(group.value).not.toBeNull();
        expect(group.value?.id).toBe('0');
        expect(group.value?.score).toBe(20);
        assertType<Project>(group.value?.project!);
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
        assertType<Project>(groups.value?.[0].project!);
        expect(groups.value?.[0].students).toBeNull;
        expect(groups.value?.[0].submissions).toBeNull();

        expect(groups.value?.[1].id).toBe('1');
        expect(groups.value?.[1].score).toBe(18);
        assertType<Project>(groups.value?.[1].project!);
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
        assertType<Project>(groups.value?.[0].project!);
        expect(groups.value?.[0].students).toBeNull;
        expect(groups.value?.[0].submissions).toBeNull();
    });
});

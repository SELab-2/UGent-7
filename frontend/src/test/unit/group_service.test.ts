import {describe, it, expect, beforeEach} from 'vitest'

import { useGroup } from '@/composables/services/groups.service.ts'
import { getgroups } from 'process';
import { Group } from '@/types/Group';

const {
    groups,
    group,
    getGroupByID,
    getGroupsByProject,
    getGroupsByStudent,

    createGroup,
    deleteGroup
} = useGroup();

describe("group", (): void => {
    it("gets group data by id", async () => {
        await getGroupByID("0")
        expect(group.value).not.toBeNull()
        expect(group.value?.score).toBe(20)
        expect(group.value?.id).toBe("0")
        expect(group.value?.project).toBeNull()
        expect(group.value?.students).toEqual([]);
        expect(group.value?.submissions).toEqual([]);
    })

    it("gets groups data by project", async () => {
        await getGroupsByProject("0")
        console.log(groups.value)
    })

    /*
    it("create group", async () => {
        let gr = new Group("3",10)
        await createGroup(gr, "0")
        console.log(group.value)
    })
    */
})
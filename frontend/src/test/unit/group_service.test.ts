import {describe, it, expect, beforeEach} from 'vitest'
import { useGroup } from '@/composables/services/groups.service.ts'

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
        // console.log(groups.value)
        // Ensure group data is not null
        expect(groups.value).not.toBeNull();
        expect(Array.isArray(groups.value)).toBe(true)
        expect(groups.value?.length).toBe(2)

        expect(groups.value?.[0]).not.toBeNull()
        expect(groups.value?.[0]?.score).toBe(20)
        expect(groups.value?.[0]?.id).toBe("0")
        expect(groups.value?.[0]?.project).toBeNull()
        expect(groups.value?.[0]?.students).toEqual([])
        expect(groups.value?.[0]?.submissions).toEqual([])

        expect(groups.value?.[1]).not.toBeNull()
        expect(groups.value?.[1]?.score).toBe(18)
        expect(groups.value?.[1]?.id).toBe("1")
        expect(groups.value?.[1]?.project).toBeNull()
        expect(groups.value?.[1]?.students).toEqual([]);
        expect(groups.value?.[1]?.submissions).toEqual([]);
    })

    /*
    it("create group", async () => {
        let gr = new Group("3",10)
        await createGroup(gr, "0")
        console.log(group.value)
    })
    */
})
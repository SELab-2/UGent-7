import {describe, it, expect, beforeEach} from 'vitest'

import { useGroup } from '@/composables/services/groups.service.ts'

describe("group", (): void => {
    it("gets group data by id", async () => {
        const response = useGroup().getGroupByID("0")
        expect(response).not.toBeNull()
    })
})
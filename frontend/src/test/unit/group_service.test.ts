import {describe, it, expect, beforeEach} from 'vitest'

import { useGroup } from '@/composables/services/groups.service.ts'

describe("admin", (): void => {
    it("gets admin data by id", async () => {
        const response = useGroup().getGroupByID("0")
        expect(response).not.toBeNull()
    })
})
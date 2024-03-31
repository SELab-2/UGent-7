import {describe, it, expect, beforeEach} from 'vitest'
import { useAssistant } from '@/composables/services/assistant.service.ts'

const {
    assistants,
    assistant,
    response,

    getAssistantByID,
    getAssistantByCourse,
    getAssistants,

    createAssistant,
    deleteAssistant,

    assistantJoinCourse,
    assistantLeaveCourse
} = useAssistant();

describe("assistant", (): void => {
    it("gets assistant data by id", async () => {
        await getAssistantByID("235")
        expect(assistant.value).not.toBeNull()
        expect(assistant.value?.username).toBe("bsimpson")
        expect(assistant.value?.is_staff).toBe(false)
        expect(assistant.value?.email).toBe("Bart.Simpson@gmail.be")
        expect(assistant.value?.first_name).toBe("Bart")
        expect(assistant.value?.last_name).toBe("Simpson")
        expect(assistant.value?.last_enrolled).toBe(2023)
        // expect(assistant.value?.last_login).toBeNull()
        // expect(assistant.value?.create_time).toEqual(new Date("July 21, 2024 01:15:00"))
        expect(assistant.value?.courses).toEqual([])
        expect(assistant.value?.faculties).toEqual([])
    })

    it("gets teacher data", async () => {
        await getAssistants()
        expect(assistants).not.toBeNull()
        expect(Array.isArray(assistants.value)).toBe(true)
        expect(assistants.value?.length).toBe(2);

        expect(assistants.value?.[0]?.username).toBe("bsimpson")
        expect(assistants.value?.[0]?.is_staff).toBe(false)
        expect(assistants.value?.[0]?.email).toBe("Bart.Simpson@gmail.be")
        expect(assistants.value?.[0]?.first_name).toBe("Bart")
        expect(assistants.value?.[0]?.last_name).toBe("Simpson")
        expect(assistants.value?.[0]?.last_enrolled).toBe(2023)
        // expect(assistants.value?.[0]?.last_login).toBeNull()
        // expect(assistants.value?.[0]?.create_time).toEqual(new Date("July 21, 2024 01:15:00"))
        expect(assistants.value?.[0]?.courses).toEqual([])
        expect(assistants.value?.[0]?.faculties).toEqual([])

        expect(assistants.value?.[1]?.username).toBe("kclijster")
        expect(assistants.value?.[1]?.is_staff).toBe(false)
        expect(assistants.value?.[1]?.email).toBe("Kim.Clijsters@gmail.be")
        expect(assistants.value?.[1]?.first_name).toBe("Kim")
        expect(assistants.value?.[1]?.last_name).toBe("Clijsters")
        expect(assistants.value?.[1]?.last_enrolled).toBe(2023)
        // expect(assistants.value?.[0]?.last_login).toBeNull()
        // expect(assistants.value?.[0]?.create_time).toEqual(new Date("July 21, 2024 01:15:00"))
        expect(assistants.value?.[1]?.courses).toEqual([])
        expect(assistants.value?.[1]?.faculties).toEqual([])
    })
})
import { Assistant } from '@/types/Assistant.ts'
import { Response } from '@/types/Response'
import { type Ref, ref } from 'vue'
import { endpoints } from '@/config/endpoints.ts'
import {
    get,
    getList,
    create,
    deleteId,
    deleteIdWithData
} from '@/composables/services/helpers.ts'

interface AssistantState {
    assistants: Ref<Assistant[] | null>
    assistant: Ref<Assistant | null>
    response: Ref<Response | null>
    getAssistantByID: (id: string) => Promise<void>
    getAssistantByCourse: (courseId: string) => Promise<void>
    getAssistants: () => Promise<void>
    assistantJoinCourse: (
        courseId: string,
        assistantId: string
    ) => Promise<void>
    assistantLeaveCourse: (
        courseId: string,
        assistantId: string
    ) => Promise<void>
    createAssistant: (assistantData: Assistant) => Promise<void>
    deleteAssistant: (id: string) => Promise<void>
}

export function useAssistant(): AssistantState {
    const assistants = ref<Assistant[] | null>(null)
    const assistant = ref<Assistant | null>(null)
    const response = ref<Response | null>(null)

    async function getAssistantByID(id: string): Promise<void> {
        const endpoint = endpoints.assistants.retrieve.replace('{id}', id)
        await get<Assistant>(endpoint, assistant, Assistant.fromJSON)
    }

    async function getAssistantByCourse(courseId: string): Promise<void> {
        const endpoint = endpoints.assistants.byCourse.replace(
            '{courseId}',
            courseId
        )
        await get<Assistant>(endpoint, assistant, Assistant.fromJSON)
    }

    async function getAssistants(): Promise<void> {
        const endpoint = endpoints.assistants.index
        await getList<Assistant>(endpoint, assistants, Assistant.fromJSON)
    }

    async function assistantJoinCourse(
        courseId: string,
        assistantId: string
    ): Promise<void> {
        const endpoint = endpoints.assistants.byCourse.replace(
            '{courseId}',
            courseId
        )
        await create<Response>(
            endpoint,
            { assistantId },
            response,
            Response.fromJSON
        )
    }

    async function assistantLeaveCourse(
        courseId: string,
        assistantId: string
    ): Promise<void> {
        const endpoint = endpoints.assistants.byCourse.replace(
            '{courseId}',
            courseId
        )
        await deleteIdWithData<Response>(
            endpoint,
            { assistantId },
            response,
            Response.fromJSON
        )
    }

    async function createAssistant(assistantData: Assistant): Promise<void> {
        const endpoint = endpoints.assistants.index
        await create<Assistant>(
            endpoint,
            {
                email: assistantData.email,
                first_name: assistantData.first_name,
                last_name: assistantData.last_name
            },
            assistant,
            Assistant.fromJSON
        )
    }

    async function deleteAssistant(id: string): Promise<void> {
        const endpoint = endpoints.admins.retrieve.replace('{id}', id)
        await deleteId<Assistant>(endpoint, assistant, Assistant.fromJSON)
    }

    return {
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
    }
}

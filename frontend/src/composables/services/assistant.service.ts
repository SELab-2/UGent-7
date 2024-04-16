import { Assistant } from '@/types/users/Assistant.ts';
import { type User } from '@/types/users/User.ts';
import { Response } from '@/types/Response';
import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList, create, deleteId, deleteIdWithData, getPaginatedList } from '@/composables/services/helpers.ts';
import { type PaginatorResponse } from '@/types/filter/Paginator.ts';
import { type Filter } from '@/types/filter/Filter.ts';

interface AssistantState {
    assistants: Ref<Assistant[] | null>;
    assistant: Ref<Assistant | null>;
    response: Ref<Response | null>;
    assistantPagination: Ref<PaginatorResponse<Assistant> | null>;
    getAssistantByID: (id: string, init?: boolean) => Promise<void>;
    getAssistantsByCourse: (courseId: string) => Promise<void>;
    getAssistants: () => Promise<void>;
    searchAssistants: (filters: Filter, page: number, pageSize: number) => Promise<void>;
    assistantJoinCourse: (courseId: string, assistantId: string) => Promise<void>;
    assistantLeaveCourse: (courseId: string, assistantId: string) => Promise<void>;
    createAssistant: (assistantData: Assistant) => Promise<void>;
    deleteAssistant: (id: string) => Promise<void>;
}

export function useAssistant(): AssistantState {
    /* State */
    const assistants = ref<Assistant[] | null>(null);
    const assistant = ref<Assistant | null>(null);
    const response = ref<Response | null>(null);
    const assistantPagination = ref<PaginatorResponse<Assistant> | null>(null);

    async function getAssistantByID(id: string): Promise<void> {
        const endpoint = endpoints.assistants.retrieve.replace('{id}', id);
        await get<Assistant>(endpoint, assistant, Assistant.fromJSON);
    }

    async function getAssistantsByCourse(courseId: string): Promise<void> {
        const endpoint = endpoints.assistants.byCourse.replace('{courseId}', courseId);
        await getList<Assistant>(endpoint, assistants, Assistant.fromJSON);
    }

    async function getAssistants(): Promise<void> {
        const endpoint = endpoints.assistants.index;
        await getList<Assistant>(endpoint, assistants, Assistant.fromJSON);
    }

    async function searchAssistants(filters: Filter, page: number, pageSize: number): Promise<void> {
        const endpoint = endpoints.assistants.search;
        await getPaginatedList<Assistant>(endpoint, filters, page, pageSize, assistantPagination, Assistant.fromJSON);
    }

    async function assistantJoinCourse(courseId: string, assistantId: string): Promise<void> {
        const endpoint = endpoints.assistants.byCourse.replace('{courseId}', courseId);
        await create<Response>(endpoint, { assistant: assistantId }, response, Response.fromJSON);
    }

    async function assistantLeaveCourse(courseId: string, assistantId: string): Promise<void> {
        const endpoint = endpoints.assistants.byCourse.replace('{courseId}', courseId);
        await deleteIdWithData<Response>(endpoint, { assistant: assistantId }, response, Response.fromJSON);
    }

    async function createAssistant(user: User): Promise<void> {
        const endpoint = endpoints.assistants.index;
        await create<Assistant>(
            endpoint,
            {
                id: user.id,
            },
            assistant,
            Assistant.fromJSON,
        );
    }

    async function deleteAssistant(id: string): Promise<void> {
        const endpoint = endpoints.assistants.retrieve.replace('{id}', id);
        await deleteId<Assistant>(endpoint, assistant, Assistant.fromJSON);
    }

    return {
        assistants,
        assistant,
        response,
        assistantPagination,

        getAssistantByID,
        getAssistantsByCourse,
        getAssistants,
        searchAssistants,

        createAssistant,
        deleteAssistant,

        assistantJoinCourse,
        assistantLeaveCourse,
    };
}

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
    getAssistantByID: (id: string, init?: boolean, selfProcessError?: boolean) => Promise<void>;
    getAssistantsByCourse: (courseId: string, selfProcessError?: boolean) => Promise<void>;
    getAssistants: (selfProcessError?: boolean) => Promise<void>;
    searchAssistants: (filters: Filter, page: number, pageSize: number, selfProcessError?: boolean) => Promise<void>;
    assistantJoinCourse: (courseId: string, assistantId: string, selfProcessError?: boolean) => Promise<void>;
    assistantLeaveCourse: (courseId: string, assistantId: string, selfProcessError?: boolean) => Promise<void>;
    createAssistant: (assistantData: Assistant, selfProcessError?: boolean) => Promise<void>;
    deleteAssistant: (id: string, selfProcessError?: boolean) => Promise<void>;
}

export function useAssistant(): AssistantState {
    /* State */
    const assistants = ref<Assistant[] | null>(null);
    const assistant = ref<Assistant | null>(null);
    const response = ref<Response | null>(null);
    const assistantPagination = ref<PaginatorResponse<Assistant> | null>(null);

    async function getAssistantByID(id: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.assistants.retrieve.replace('{id}', id);
        await get<Assistant>(endpoint, assistant, Assistant.fromJSON, selfProcessError);
    }

    async function getAssistantsByCourse(courseId: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.assistants.byCourse.replace('{courseId}', courseId);
        await getList<Assistant>(endpoint, assistants, Assistant.fromJSON, selfProcessError);
    }

    async function getAssistants(selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.assistants.index;
        await getList<Assistant>(endpoint, assistants, Assistant.fromJSON, selfProcessError);
    }

    async function searchAssistants(
        filters: Filter,
        page: number,
        pageSize: number,
        selfProcessError: boolean = true,
    ): Promise<void> {
        const endpoint = endpoints.assistants.search;
        await getPaginatedList<Assistant>(
            endpoint,
            filters,
            page,
            pageSize,
            assistantPagination,
            Assistant.fromJSON,
            selfProcessError,
        );
    }

    async function assistantJoinCourse(
        courseId: string,
        assistantId: string,
        selfProcessError: boolean = true,
    ): Promise<void> {
        const endpoint = endpoints.assistants.byCourse.replace('{courseId}', courseId);
        await create<Response>(
            endpoint,
            { assistant: assistantId },
            response,
            Response.fromJSON,
            undefined,
            selfProcessError,
        );
    }

    async function assistantLeaveCourse(
        courseId: string,
        assistantId: string,
        selfProcessError: boolean = true,
    ): Promise<void> {
        const endpoint = endpoints.assistants.byCourse.replace('{courseId}', courseId);
        await deleteIdWithData<Response>(
            endpoint,
            { assistant: assistantId },
            response,
            Response.fromJSON,
            selfProcessError,
        );
    }

    async function createAssistant(user: User, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.assistants.index;
        await create<Assistant>(
            endpoint,
            {
                user: user.id,
            },
            assistant,
            Assistant.fromJSON,
            undefined,
            selfProcessError,
        );
    }

    async function deleteAssistant(id: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.assistants.retrieve.replace('{id}', id);
        await deleteId<Assistant>(endpoint, assistant, Assistant.fromJSON, selfProcessError);
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

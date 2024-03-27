import {Assistant} from '@/types/Assistant.ts';
import { Response } from '@/types/Response';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id, delete_id_with_data } from '@/composables/services/helpers.ts';

export function useAssistant() {
    const assistants = ref<Assistant[]|null>(null);
    const assistant = ref<Assistant|null>(null);
    const response = ref<Response|null>(null);

    async function getAssistantByID(id: string) {
        const endpoint = endpoints.assistants.retrieve.replace('{id}', id);
        await get<Assistant>(endpoint, assistant, Assistant.fromJSON);
    }

    async function getAssistantByCourse(course_id: string) {
        const endpoint = endpoints.assistants.byCourse.replace('{course_id}', course_id);
        await get<Assistant>(endpoint, assistant, Assistant.fromJSON);
    }

    async function getAssistants() {
        const endpoint = endpoints.assistants.index;
        await getList<Assistant>(endpoint, assistants, Assistant.fromJSON);
    }

    async function assistantJoinCourse(course_id: string, assistant_id: string) {
        const endpoint = endpoints.assistants.byCourse.replace('{course_id}', course_id);
        await create<Response>(endpoint, {assistant_id: assistant_id}, response, Response.fromJSON);
    }

    async function assistantLeaveCourse(course_id: string, assistant_id: string) {
        const endpoint = endpoints.assistants.byCourse.replace('{course_id}', course_id);
        await delete_id_with_data<Response>(endpoint, {assistant_id: assistant_id}, response, Response.fromJSON);
    }

    async function createAssistant(assistant_data: any) {
        const endpoint = endpoints.assistants.index;
        await create<Assistant>(endpoint, assistant_data, assistant, Assistant.fromJSON);
    }

    async function deleteAssistant(id: string) {
        const endpoint = endpoints.admins.retrieve.replace('{id}', id);
        await delete_id<Assistant>(endpoint, assistant, Assistant.fromJSON);
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
    };
}
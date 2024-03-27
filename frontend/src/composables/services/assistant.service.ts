import {Assistant} from '@/types/Assistant.ts';
import { Response } from '@/types/Response';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id, delete_id_with_data } from '@/composables/services/helpers.ts';
import {ComposerTranslation} from "vue-i18n";

export function useAssistant() {
    const assistants = ref<Assistant[]|null>(null);
    const assistant = ref<Assistant|null>(null);
    const response = ref<Response|null>(null);

    async function getAssistantByID(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.assistants.retrieve.replace('{id}', id);
        await get<Assistant>(endpoint, assistant, Assistant.fromJSON, t);
    }

    async function getAssistantByCourse(course_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.assistants.byCourse.replace('{course_id}', course_id);
        await get<Assistant>(endpoint, assistant, Assistant.fromJSON, t);
    }

    async function getAssistants(t: ComposerTranslation) {
        const endpoint = endpoints.assistants.index;
        await getList<Assistant>(endpoint, assistants, Assistant.fromJSON, t);
    }

    async function assistantJoinCourse(course_id: string, assistant_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.assistants.byCourse.replace('{course_id}', course_id);
        await create<Response>(endpoint, {assistant_id: assistant_id}, response, Response.fromJSON, t);
    }

    async function assistantLeaveCourse(course_id: string, assistant_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.assistants.byCourse.replace('{course_id}', course_id);
        await delete_id_with_data<Response>(endpoint, {assistant_id: assistant_id}, response, Response.fromJSON, t);
    }

    async function createAssistant(assistant_data: any, t: ComposerTranslation) {
        const endpoint = endpoints.assistants.index;
        await create<Assistant>(endpoint, assistant_data, assistant, Assistant.fromJSON, t);
    }

    async function deleteAssistant(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.admins.retrieve.replace('{id}', id);
        await delete_id<Assistant>(endpoint, assistant, Assistant.fromJSON, t);
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
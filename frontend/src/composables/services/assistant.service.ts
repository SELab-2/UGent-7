import {Assistant} from '@/types/Assistant.ts';
import { Response } from '@/types/Response';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';
import {ComposerTranslation} from "vue-i18n";

export function useAssistant() {
    const assistants = ref<Assistant[]|null>(null);
    const assistant = ref<Assistant|null>(null);
    const response = ref<Response|null>(null);
    const toast = useToast();

    async function getAssistantByID(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.assistants.retrieve.replace('{id}', id);
        get<Assistant>(endpoint, assistant, Assistant.fromJSON, toast, t);
    }

    async function getAssistantByCourse(course_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.assistants.byCourse.replace('{course_id}', course_id);
        get<Assistant>(endpoint, assistant, Assistant.fromJSON, toast, t);
    }

    async function getAssistants(t: ComposerTranslation) {
        const endpoint = endpoints.assistants.index;
        getList<Assistant>(endpoint, assistants, Assistant.fromJSON, toast, t);
    }

    async function assistantJoinCourse(course_id: string, assistant_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.assistants.byCourse.replace('{course_id}', course_id);
        create<Response>(endpoint, {assistant_id: assistant_id}, response, Response.fromJSON, toast, t);
    }

    async function createAssistant(assistant_data: any, t: ComposerTranslation) {
        const endpoint = endpoints.assistants.index;
        create<Assistant>(endpoint, assistant_data, assistant, Assistant.fromJSON, toast, t);
    }

    async function deleteAssistant(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.admins.retrieve.replace('{id}', id);
        delete_id<Assistant>(endpoint, assistant, Assistant.fromJSON, toast, t);
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

        assistantJoinCourse
    };
}
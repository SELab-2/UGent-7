import {Assistant} from '@/types/Assistant.ts';
import { Response } from '@/types/Response';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';

export function useAssistant() {
    const assistants = ref<Assistant[]|null>(null);
    const assistant = ref<Assistant|null>(null);
    const response = ref<Response|null>(null);
    const toast = useToast();

    async function getAssistantByID(id: string) {
        const endpoint = endpoints.assistants.retrieve.replace('{id}', id);
        get<Assistant>(endpoint, assistant, Assistant.fromJSON, toast);
    }

    async function getAssistantByCourse(course_id: string) {
        const endpoint = endpoints.assistants.byCourse.replace('{course_id}', course_id);
        get<Assistant>(endpoint, assistant, Assistant.fromJSON, toast);
    }

    async function getAssistants() {
        const endpoint = endpoints.assistants.index;
        getList<Assistant>(endpoint, assistants, Assistant.fromJSON, toast);
    }

    async function assistantJoinCourse(course_id: string, teacher_id: string) {
        const endpoint = endpoints.assistants.byCourse.replace('{course_id}', course_id);
        create<Response>(endpoint, {teacher_id: teacher_id}, response, Response.fromJSON, toast);
    }

    async function createAssistant(assistant_data: any) {
        const endpoint = endpoints.assistants.index;
        create<Assistant>(endpoint, assistant_data, assistant, Assistant.fromJSON, toast);
    }

    async function deleteAssistant(id: string) {
        const endpoint = endpoints.admins.retrieve.replace('{id}', id.toString());
        delete_id<Assistant>(endpoint, assistant, Assistant.fromJSON, toast);
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
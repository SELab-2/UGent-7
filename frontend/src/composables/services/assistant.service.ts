import {Assistant} from '@/types/Assistant.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';

export function useAssistant() {
    const assistants = ref<Assistant[]|null>(null);
    const assistant = ref<Assistant|null>(null);
    const toast = useToast();

    async function getAssistantByID(id: number) {
        const endpoint = endpoints.assistants.retrieve.replace('{id}', id.toString());
        get<Assistant>(endpoint, assistant, Assistant.fromJSON, toast);
        console.log(assistant)
    }

    async function getAssistants() {
        const endpoint = endpoints.assistants.index;
        getList<Assistant>(endpoint, assistants, Assistant.fromJSON, toast);
        console.log(assistants.value ? assistants.value.map((assistant, index) => `Assistant ${index + 1}: ${JSON.stringify(assistant)}`) : 'assistants is null');
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
        getAssistantByID,
        getAssistants,

        createAssistant,
        deleteAssistant
    };
}
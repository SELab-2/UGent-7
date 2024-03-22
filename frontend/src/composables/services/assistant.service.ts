import {Assistant} from '@/types/Assistant.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList } from '@/composables/services/helpers.ts';

export function useAssistant() {
    const assistants = ref<Assistant[]|null>(null);
    const assistant = ref<Assistant|null>(null);

    async function getAssistantByID(id: number) {
        const endpoint = endpoints.assistants.retrieve.replace('{id}', id.toString());
        get<Assistant>(endpoint, assistant, Assistant.fromJSON);
        console.log(assistant)
    }

    async function getAssistants() {
        const endpoint = endpoints.assistants.index;
        getList<Assistant>(endpoint, assistants, Assistant.fromJSON);
        console.log(assistants.value ? assistants.value.map((assistant, index) => `Assistant ${index + 1}: ${JSON.stringify(assistant)}`) : 'assistants is null');
    }

    return {
        assistants,
        assistant,
        getAssistantByID,
        getAssistants
    };
}
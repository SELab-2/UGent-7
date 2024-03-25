import {Assistant} from '@/types/Assistant.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';
import {ComposerTranslation} from "vue-i18n";

export function useAssistant() {
    const assistants = ref<Assistant[]|null>(null);
    const assistant = ref<Assistant|null>(null);
    const toast = useToast();

    async function getAssistantByID(id: number, t: ComposerTranslation) {
        const endpoint = endpoints.assistants.retrieve.replace('{id}', id.toString());
        get<Assistant>(endpoint, assistant, Assistant.fromJSON, toast, t);
        console.log(assistant)
    }

    async function getAssistants(t: ComposerTranslation) {
        const endpoint = endpoints.assistants.index;
        getList<Assistant>(endpoint, assistants, Assistant.fromJSON, toast, t);
        console.log(assistants.value ? assistants.value.map((assistant, index) => `Assistant ${index + 1}: ${JSON.stringify(assistant)}`) : 'assistants is null');
    }

    return {
        assistants,
        assistant,
        getAssistantByID,
        getAssistants
    };
}
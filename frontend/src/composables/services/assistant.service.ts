import {Assistant} from '@/types/Assistant.ts';
import {ref} from 'vue';
import axios from 'axios';
import {endpoints} from '@/config/endpoints.ts';

export function useAssistant() {
    const assistants = ref<Assistant[]|null>(null);
    const assistant = ref<Assistant|null>(null);

    async function getAssistantByID(id: number) {
        const endpoint = endpoints.assistants.retrieve.replace('{id}', id.toString());

        axios.get(endpoint).then(response => {
            assistant.value = Assistant.fromJSON(response.data);
        }).catch(error => {
            console.log(error.data);
        });

        console.log(assistant)
    }

    async function getAssistants() {
        const endpoint = endpoints.assistants.index;

        axios.get(endpoint).then(response => {
            assistants.value = response.data.map((assistantData: Assistant) => Assistant.fromJSON(assistantData));
        }).catch(error => {
            console.log(error.data);
        });

        console.log(assistants.value ? assistants.value.map((assistant, index) => `Assistant ${index + 1}: ${JSON.stringify(assistant)}`) : 'assistants is null');
    }

    return {
        assistants,
        assistant,
        getAssistantByID,
        getAssistants
    };
}
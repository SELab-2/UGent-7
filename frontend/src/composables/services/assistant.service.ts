import {Assistant} from '@/types/Assistant.ts';
import {ref} from 'vue';
import axios from 'axios';
import {endpoints} from '@/config/endpoints.ts';

export function useAssistant() {
    const assistants = ref<Assistant[]|null>(null);
    const assistant = ref<Assistant|null>(null);

    async function getAssistentByID(id: number) {
        const endpoint = endpoints.assistants.retrieve.replace('{id}', id.toString());

        axios.get(endpoint).then(response => {
            assistant.value = Assistant.fromJSON(response.data);
        }).catch(error => {
            console.log(error.data);
        });

        console.log(assistant)
    }

    return {
        assistants,
        assistant,
        getAssistentByID
    };
}
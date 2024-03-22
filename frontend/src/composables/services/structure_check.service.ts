import {Structure_check} from '@/types/Structure_check.ts';
import {ref} from 'vue';
import axios from 'axios';
import {endpoints} from '@/config/endpoints.ts';

export function useStructure_check() {
    const structure_checks = ref<Structure_check[]|null>(null);
    const structure_check = ref<Structure_check|null>(null);

    async function getStructure_checkByID(id: number) {
        const endpoint = endpoints.structure_checks.retrieve.replace('{id}', id.toString());

        axios.get(endpoint).then(response => {
            structure_check.value = Structure_check.fromJSON(response.data);
        }).catch(error => {
            console.log(error.data);
        });

        console.log(structure_check)
    }

    async function getStructure_checkByProject(project_id: number) {
        const endpoint = endpoints.structure_checks.byProject.replace('{project_id}', project_id.toString());

        axios.get(endpoint).then(response => {
            structure_checks.value = response.data.map((structure_checkData: Structure_check) => Structure_check.fromJSON(structure_checkData));
        }).catch(error => {
            console.log(error.data);
        });

        console.log(structure_checks.value ? structure_checks.value.map((structure_check, index) => `Structure_check ${index + 1}: ${JSON.stringify(structure_check)}`) : 'Structure_check is null');
    }

    return {
        structure_checks,
        structure_check,
        getStructure_checkByID,
        getStructure_checkByProject
    };
}
import {Structure_check} from '@/types/Structure_check.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList } from '@/composables/services/helpers.ts';

export function useStructure_check() {
    const structure_checks = ref<Structure_check[]|null>(null);
    const structure_check = ref<Structure_check|null>(null);

    async function getStructure_checkByID(id: number) {
        const endpoint = endpoints.structure_checks.retrieve.replace('{id}', id.toString());
        get<Structure_check>(endpoint, structure_check, Structure_check.fromJSON);
        console.log(structure_check)
    }

    async function getStructure_checkByProject(project_id: number) {
        const endpoint = endpoints.structure_checks.byProject.replace('{project_id}', project_id.toString());
        getList<Structure_check>(endpoint, structure_checks, Structure_check.fromJSON);
        console.log(structure_checks.value ? structure_checks.value.map((structure_check, index) => `Structure_check ${index + 1}: ${JSON.stringify(structure_check)}`) : 'Structure_check is null');
    }

    return {
        structure_checks,
        structure_check,
        getStructure_checkByID,
        getStructure_checkByProject
    };
}
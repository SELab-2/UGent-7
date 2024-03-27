import {Structure_check} from '@/types/Structure_check.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';

export function useStructure_check() {
    const structure_checks = ref<Structure_check[]|null>(null);
    const structure_check = ref<Structure_check|null>(null);

    async function getStructure_checkByID(id: string) {
        const endpoint = endpoints.structure_checks.retrieve.replace('{id}', id);
        await get<Structure_check>(endpoint, structure_check, Structure_check.fromJSON);
    }

    async function getStructure_checkByProject(project_id: string) {
        const endpoint = endpoints.structure_checks.byProject.replace('{project_id}', project_id);
        await getList<Structure_check>(endpoint, structure_checks, Structure_check.fromJSON);
    }

    async function createStructure_check(structure_check_data: any, project_id: string) {
        const endpoint = endpoints.structure_checks.byProject.replace('{project_id}', project_id);
        await create<Structure_check>(endpoint, structure_check_data, structure_check, Structure_check.fromJSON);
    }

    async function deleteStructure_check(id: string) {
        const endpoint = endpoints.structure_checks.retrieve.replace('{id}', id);
        await delete_id<Structure_check>(endpoint, structure_check, Structure_check.fromJSON);
    }

    return {
        structure_checks,
        structure_check,
        getStructure_checkByID,
        getStructure_checkByProject,

        createStructure_check,
        deleteStructure_check
    };
}
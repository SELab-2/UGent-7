import {StructureCheck} from '@/types/StructureCheck.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';

export function useStructureCheck() {
    const structure_checks = ref<StructureCheck[]|null>(null);
    const structure_check = ref<StructureCheck|null>(null);

    async function getStructureCheckByID(id: string) {
        const endpoint = endpoints.structure_checks.retrieve.replace('{id}', id);
        await get<StructureCheck>(endpoint, structure_check, StructureCheck.fromJSON);
    }

    async function getStructureCheckByProject(project_id: string) {
        const endpoint = endpoints.structure_checks.byProject.replace('{project_id}', project_id);
        await getList<StructureCheck>(endpoint, structure_checks, StructureCheck.fromJSON);
    }

    async function createStructureCheck(structure_check_data: StructureCheck, project_id: string) {
        const endpoint = endpoints.structure_checks.byProject.replace('{project_id}', project_id);
        await create<StructureCheck>(endpoint, 
            {
                name: structure_check_data.name
            },
        structure_check, StructureCheck.fromJSON);
    }

    async function deleteStructureCheck(id: string) {
        const endpoint = endpoints.structure_checks.retrieve.replace('{id}', id);
        await delete_id<StructureCheck>(endpoint, structure_check, StructureCheck.fromJSON);
    }

    return {
        structure_checks,
        structure_check,
        getStructureCheckByID,
        getStructureCheckByProject,

        createStructureCheck,
        deleteStructureCheck
    };
}
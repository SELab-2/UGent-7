import {Structure_check} from '@/types/Structure_check.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';

export function useStructure_check() {
    const structure_checks = ref<Structure_check[]|null>(null);
    const structure_check = ref<Structure_check|null>(null);
    const toast = useToast();

    async function getStructure_checkByID(id: number) {
        const endpoint = endpoints.structure_checks.retrieve.replace('{id}', id.toString());
        get<Structure_check>(endpoint, structure_check, Structure_check.fromJSON, toast);
    }

    async function getStructure_checkByProject(project_id: number) {
        const endpoint = endpoints.structure_checks.byProject.replace('{project_id}', project_id.toString());
        getList<Structure_check>(endpoint, structure_checks, Structure_check.fromJSON, toast);
    }

    async function createStructure_check(structure_check_data: any, project_id: string) {
        const endpoint = endpoints.structure_checks.byProject.replace('{project_id}', project_id);
        create<Structure_check>(endpoint, structure_check_data, structure_check, Structure_check.fromJSON, toast);
    }

    async function deleteStructure_check(id: string) {
        const endpoint = endpoints.structure_checks.retrieve.replace('{id}', id.toString());
        delete_id<Structure_check>(endpoint, structure_check, Structure_check.fromJSON, toast);
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
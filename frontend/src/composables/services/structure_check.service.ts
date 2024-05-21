import { StructureCheck } from '@/types/StructureCheck.ts';
import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList, create, deleteId } from '@/composables/services/helpers.ts';

interface StructureCheckState {
    structureChecks: Ref<StructureCheck[] | null>;
    structureCheck: Ref<StructureCheck | null>;
    getStructureCheckByID: (id: string, selfprocessError?: boolean) => Promise<void>;
    getStructureCheckByProject: (projectId: string, selfprocessError?: boolean) => Promise<void>;
    createStructureCheck: (
        structureCheckData: StructureCheck,
        projectId: string,
        selfprocessError?: boolean,
    ) => Promise<void>;
    deleteStructureCheck: (id: string, selfprocessError?: boolean) => Promise<void>;
}

export function useStructureCheck(): StructureCheckState {
    const structureChecks = ref<StructureCheck[] | null>(null);
    const structureCheck = ref<StructureCheck | null>(null);

    async function getStructureCheckByID(id: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.structureChecks.retrieve.replace('{id}', id);
        await get<StructureCheck>(endpoint, structureCheck, StructureCheck.fromJSON, selfprocessError);
    }

    async function getStructureCheckByProject(projectId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.structureChecks.byProject.replace('{projectId}', projectId);
        await getList<StructureCheck>(endpoint, structureChecks, StructureCheck.fromJSON, selfprocessError);
    }

    async function createStructureCheck(
        structureCheckData: StructureCheck,
        projectId: string,
        selfprocessError: boolean = true,
    ): Promise<void> {
        const endpoint = endpoints.structureChecks.byProject.replace('{projectId}', projectId);
        await create<StructureCheck>(
            endpoint,
            {
                name: structureCheckData.name,
            },
            structureCheck,
            StructureCheck.fromJSON,
            undefined,
            selfprocessError,
        );
    }

    async function deleteStructureCheck(id: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.structureChecks.retrieve.replace('{id}', id);
        await deleteId<StructureCheck>(endpoint, structureCheck, StructureCheck.fromJSON, selfprocessError);
    }

    return {
        structureChecks,
        structureCheck,
        getStructureCheckByID,
        getStructureCheckByProject,

        createStructureCheck,
        deleteStructureCheck,
    };
}

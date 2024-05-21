import { StructureCheck } from '@/types/StructureCheck.ts';
import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList, create, deleteId, put } from '@/composables/services/helpers.ts';

interface StructureCheckState {
    structureChecks: Ref<StructureCheck[] | null>;
    structureCheck: Ref<StructureCheck | null>;
    getStructureCheckByID: (id: string) => Promise<void>;
    getStructureCheckByProject: (projectId: string) => Promise<void>;
    createStructureCheck: (structureCheckData: StructureCheck, projectId: string) => Promise<void>;
    setStructureChecks: (structureChecks: StructureCheck[], projectId: string) => Promise<void>;
    deleteStructureCheck: (id: string) => Promise<void>;
}

export function useStructureCheck(): StructureCheckState {
    const structureChecks = ref<StructureCheck[] | null>(null);
    const structureCheck = ref<StructureCheck | null>(null);

    async function getStructureCheckByID(id: string): Promise<void> {
        const endpoint = endpoints.structureChecks.retrieve.replace('{id}', id);
        await get<StructureCheck>(endpoint, structureCheck, StructureCheck.fromJSON);
    }

    async function getStructureCheckByProject(projectId: string): Promise<void> {
        const endpoint = endpoints.structureChecks.byProject.replace('{projectId}', projectId);
        await getList<StructureCheck>(endpoint, structureChecks, StructureCheck.fromJSON);
    }

    async function createStructureCheck(structureCheckData: StructureCheck, projectId: string): Promise<void> {
        const endpoint = endpoints.structureChecks.byProject.replace('{projectId}', projectId);
        await create<StructureCheck>(
            endpoint,
            {
                path: structureCheckData.path,
            },
            structureCheck,
            StructureCheck.fromJSON,
        );
    }

    async function setStructureChecks(structureChecks: StructureCheck[], projectId: string): Promise<void> {
        const endpoint = endpoints.structureChecks.byProject.replace('{projectId}', projectId);
        await put(endpoint, structureChecks);
    }

    async function deleteStructureCheck(id: string): Promise<void> {
        const endpoint = endpoints.structureChecks.retrieve.replace('{id}', id);
        await deleteId<StructureCheck>(endpoint, structureCheck, StructureCheck.fromJSON);
    }

    return {
        structureChecks,
        structureCheck,
        getStructureCheckByID,
        getStructureCheckByProject,

        createStructureCheck,
        deleteStructureCheck,
        setStructureChecks
    };
}

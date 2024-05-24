import { StructureCheck } from '@/types/StructureCheck.ts';
import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList, create, deleteId, put } from '@/composables/services/helpers.ts';

interface StructureCheckState {
    structureChecks: Ref<StructureCheck[] | null>;
    structureCheck: Ref<StructureCheck | null>;

    getStructureCheckByID: (id: string, selfProcessError?: boolean) => Promise<void>;
    getStructureCheckByProject: (projectId: string, selfProcessError?: boolean) => Promise<void>;
    createStructureCheck: (
        structureCheckData: StructureCheck,
        projectId: string,
        selfProcessError?: boolean,
    ) => Promise<void>;
    setStructureChecks: (
        structureChecks: StructureCheck[],
        projectId: string,
        selfProcessError?: boolean,
    ) => Promise<void>;
    deleteStructureCheck: (id: string, selfProcessError?: boolean) => Promise<void>;
}

export function useStructureCheck(): StructureCheckState {
    const structureChecks = ref<StructureCheck[] | null>(null);
    const structureCheck = ref<StructureCheck | null>(null);

    async function getStructureCheckByID(id: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.structureChecks.retrieve.replace('{id}', id);
        await get<StructureCheck>(endpoint, structureCheck, StructureCheck.fromJSON, selfProcessError);
    }

    async function getStructureCheckByProject(projectId: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.structureChecks.byProject.replace('{projectId}', projectId);
        await getList<StructureCheck>(endpoint, structureChecks, StructureCheck.fromJSON, selfProcessError);
    }

    async function createStructureCheck(
        structureCheckData: StructureCheck,
        projectId: string,
        selfProcessError: boolean = true,
    ): Promise<void> {
        const endpoint = endpoints.structureChecks.byProject.replace('{projectId}', projectId);
        await create<StructureCheck>(
            endpoint,
            {
                path: structureCheckData.path,
                obligated_extensions: structureCheckData.obligated_extensions?.map((ext) => ext.extension),
                blocked_extensions: structureCheckData.blocked_extensions?.map((ext) => ext.extension),
            },
            structureCheck,
            StructureCheck.fromJSON,
            undefined,
            selfProcessError,
        );
    }

    async function setStructureChecks(
        structureChecks: StructureCheck[],
        projectId: string,
        selfProcessError: boolean = true,
    ): Promise<void> {
        const endpoint = endpoints.structureChecks.byProject.replace('{projectId}', projectId);
        await put(endpoint, structureChecks, undefined, selfProcessError);
    }

    async function deleteStructureCheck(id: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.structureChecks.retrieve.replace('{id}', id);
        await deleteId<StructureCheck>(endpoint, structureCheck, StructureCheck.fromJSON, selfProcessError);
    }

    return {
        structureChecks,
        structureCheck,
        getStructureCheckByID,
        getStructureCheckByProject,

        createStructureCheck,
        deleteStructureCheck,
        setStructureChecks,
    };
}

import { StructureCheck } from '@/types/StructureCheck.ts'
import { ref } from 'vue'
import { endpoints } from '@/config/endpoints.ts'
import {
    get,
    getList,
    create,
    deleteId
} from '@/composables/services/helpers.ts'

export function useStructureCheck() {
    const structureChecks = ref<StructureCheck[] | null>(null)
    const structureCheck = ref<StructureCheck | null>(null)

    async function getStructureCheckByID(id: string) {
        const endpoint = endpoints.structureChecks.retrieve.replace('{id}', id)
        await get<StructureCheck>(
            endpoint,
            structureCheck,
            StructureCheck.fromJSON
        )
    }

    async function getStructureCheckByProject(projectId: string) {
        const endpoint = endpoints.structureChecks.byProject.replace(
            '{projectId}',
            projectId
        )
        await getList<StructureCheck>(
            endpoint,
            structureChecks,
            StructureCheck.fromJSON
        )
    }

    async function createStructureCheck(
        structureCheckData: StructureCheck,
        projectId: string
    ) {
        const endpoint = endpoints.structureChecks.byProject.replace(
            '{projectId}',
            projectId
        )
        await create<StructureCheck>(
            endpoint,
            {
                name: structureCheckData.name
            },
            structureCheck,
            StructureCheck.fromJSON
        )
    }

    async function deleteStructureCheck(id: string) {
        const endpoint = endpoints.structureChecks.retrieve.replace('{id}', id)
        await deleteId<StructureCheck>(
            endpoint,
            structureCheck,
            StructureCheck.fromJSON
        )
    }

    return {
        structureChecks,
        structureCheck,
        getStructureCheckByID,
        getStructureCheckByProject,

        createStructureCheck,
        deleteStructureCheck
    }
}

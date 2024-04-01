import { Group } from '@/types/Group.ts'
import { ref } from 'vue'
import { endpoints } from '@/config/endpoints.ts'
import {
    get,
    getList,
    create,
    deleteId
} from '@/composables/services/helpers.ts'

export function useGroup() {
    const groups = ref<Group[] | null>(null)
    const group = ref<Group | null>(null)

    async function getGroupByID(id: string) {
        const endpoint = endpoints.groups.retrieve.replace('{id}', id)
        await get<Group>(endpoint, group, Group.fromJSON)
    }

    async function getGroupsByProject(projectId: string) {
        const endpoint = endpoints.groups.byProject.replace(
            '{projectId}',
            projectId
        )
        await getList<Group>(endpoint, groups, Group.fromJSON)
    }

    async function getGroupsByStudent(studentId: string) {
        const endpoint = endpoints.groups.byStudent.replace(
            '{studentId}',
            studentId
        )
        await getList<Group>(endpoint, groups, Group.fromJSON)
    }

    async function createGroup(groupData: Group, projectId: string) {
        const endpoint = endpoints.groups.byProject.replace(
            '{projectId}',
            projectId
        )
        await create<Group>(
            endpoint,
            {
                score: groupData.score
            },
            group,
            Group.fromJSON
        )
    }

    async function deleteGroup(id: string) {
        const endpoint = endpoints.groups.retrieve.replace('{id}', id)
        await deleteId<Group>(endpoint, group, Group.fromJSON)
    }

    return {
        groups,
        group,
        getGroupByID,
        getGroupsByProject,
        getGroupsByStudent,

        createGroup,
        deleteGroup
    }
}

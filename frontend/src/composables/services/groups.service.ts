import { Group } from '@/types/Group.ts'
import { ref } from 'vue'
import { endpoints } from '@/config/endpoints.ts'
import {
    get,
    getList,
    create,
    delete_id
} from '@/composables/services/helpers.ts'

export function useGroup() {
    const groups = ref<Group[] | null>(null)
    const group = ref<Group | null>(null)

    async function getGroupByID(id: string) {
        const endpoint = endpoints.groups.retrieve.replace('{id}', id)
        await get<Group>(endpoint, group, Group.fromJSON)
    }

    async function getGroupsByProject(project_id: string) {
        const endpoint = endpoints.groups.byProject.replace(
            '{project_id}',
            project_id
        )
        await getList<Group>(endpoint, groups, Group.fromJSON)
    }

    async function getGroupsByStudent(student_id: string) {
        const endpoint = endpoints.groups.byStudent.replace(
            '{student_id}',
            student_id
        )
        await getList<Group>(endpoint, groups, Group.fromJSON)
    }

    async function createGroup(group_data: Group, project_id: string) {
        const endpoint = endpoints.groups.byProject.replace(
            '{project_id}',
            project_id
        )
        await create<Group>(
            endpoint,
            {
                score: group_data.score
            },
            group,
            Group.fromJSON
        )
    }

    async function deleteGroup(id: string) {
        const endpoint = endpoints.groups.retrieve.replace('{id}', id)
        await delete_id<Group>(endpoint, group, Group.fromJSON)
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

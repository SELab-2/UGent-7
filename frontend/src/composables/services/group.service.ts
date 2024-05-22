import { Group } from '@/types/Group.ts';
import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList, create, deleteId, patch } from '@/composables/services/helpers.ts';
import type { Response } from '@/types/Response.ts';

interface GroupState {
    groups: Ref<Group[] | null>;
    group: Ref<Group | null>;
    getGroupByID: (id: string) => Promise<void>;
    getGroupsByProject: (projectId: string) => Promise<void>;
    getGroupsByStudent: (studentId: string) => Promise<void>;
    getGroupByStudentProject: (projectId: string) => Promise<void>;
    createGroup: (groupData: Group, projectId: string) => Promise<void>;
    updateGroup: (groupData: Partial<Group>) => Promise<void>;
    deleteGroup: (id: string) => Promise<void>;
}

export function useGroup(): GroupState {
    const groups = ref<Group[] | null>(null);
    const group = ref<Group | null>(null);
    const response = ref<Response | null>(null);

    async function getGroupByID(id: string): Promise<void> {
        const endpoint = endpoints.groups.retrieve.replace('{id}', id);
        await get<Group>(endpoint, group, Group.fromJSON);
    }

    async function getGroupsByProject(projectId: string): Promise<void> {
        const endpoint = endpoints.groups.byProject.replace('{projectId}', projectId);
        await getList<Group>(endpoint, groups, Group.fromJSON);
    }

    async function getGroupsByStudent(studentId: string): Promise<void> {
        const endpoint = endpoints.groups.byStudent.replace('{studentId}', studentId);
        await getList<Group>(endpoint, groups, Group.fromJSON);
    }

    async function getGroupByStudentProject(projectId: string): Promise<void> {
        const endpoint = endpoints.groups.byProjectStudent.replace('{projectId}', projectId);
        await get<Group>(endpoint, group, Group.fromJSON);
    }

    async function createGroup(groupData: Group, projectId: string): Promise<void> {
        const endpoint = endpoints.groups.byProject.replace('{projectId}', projectId);
        await create<Group>(
            endpoint,
            {
                score: groupData.score,
                project: groupData.project?.id,
            },
            group,
            Group.fromJSON,
        );
    }

    async function updateGroup(groupData: Partial<Group>): Promise<void> {
        if (groupData.id !== undefined) {
            const endpoint = endpoints.groups.retrieve.replace('{id}', groupData.id);
            await patch(
                endpoint,
                {
                    score: groupData.score,
                },
                response,
            );
        }
    }

    async function deleteGroup(id: string): Promise<void> {
        const endpoint = endpoints.groups.retrieve.replace('{id}', id);
        await deleteId<Group>(endpoint, group, Group.fromJSON);
    }

    return {
        groups,
        group,
        getGroupByID,
        getGroupsByProject,
        getGroupsByStudent,
        getGroupByStudentProject,

        createGroup,
        deleteGroup,
        updateGroup,
    };
}

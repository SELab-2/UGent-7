import { Group } from '@/types/Group.ts';
import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList, create, deleteId } from '@/composables/services/helpers.ts';

interface GroupState {
    groups: Ref<Group[] | null>;
    group: Ref<Group | null>;
    getGroupByID: (id: string, selfprocessError?: boolean) => Promise<void>;
    getGroupsByProject: (projectId: string, selfprocessError?: boolean) => Promise<void>;
    getGroupsByStudent: (studentId: string, selfprocessError?: boolean) => Promise<void>;
    createGroup: (groupData: Group, projectId: string, selfprocessError?: boolean) => Promise<void>;
    deleteGroup: (id: string, selfprocessError?: boolean) => Promise<void>;
}

export function useGroup(): GroupState {
    const groups = ref<Group[] | null>(null);
    const group = ref<Group | null>(null);

    async function getGroupByID(id: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.groups.retrieve.replace('{id}', id);
        await get<Group>(endpoint, group, Group.fromJSON, selfprocessError);
    }

    async function getGroupsByProject(projectId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.groups.byProject.replace('{projectId}', projectId);
        await getList<Group>(endpoint, groups, Group.fromJSON, selfprocessError);
    }

    async function getGroupsByStudent(studentId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.groups.byStudent.replace('{studentId}', studentId);
        await getList<Group>(endpoint, groups, Group.fromJSON, selfprocessError);
    }

    async function createGroup(groupData: Group, projectId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.groups.byProject.replace('{projectId}', projectId);
        await create<Group>(
            endpoint,
            {
                score: groupData.score,
                project: groupData.project?.id,
            },
            group,
            Group.fromJSON,
            undefined,
            selfprocessError,
        );
    }

    async function deleteGroup(id: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.groups.retrieve.replace('{id}', id);
        await deleteId<Group>(endpoint, group, Group.fromJSON, selfprocessError);
    }

    return {
        groups,
        group,
        getGroupByID,
        getGroupsByProject,
        getGroupsByStudent,

        createGroup,
        deleteGroup,
    };
}

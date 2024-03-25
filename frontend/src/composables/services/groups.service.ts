import {Group} from '@/types/Group.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';

export function useGroup() {
    const groups = ref<Group[]|null>(null);
    const group = ref<Group|null>(null);
    const toast = useToast();

    async function getGroupByID(id: number) {
        const endpoint = endpoints.groups.retrieve.replace('{id}', id.toString());
        get<Group>(endpoint, group, Group.fromJSON, toast);
    }

    async function getGroupsByProject(project_id: number) {
        const endpoint = endpoints.groups.byProject.replace('{project_id}', project_id.toString());
        getList<Group>(endpoint, groups, Group.fromJSON, toast);
    }

    async function createGroup(group_data: any, group_id: string) {
        const endpoint = endpoints.groups.byProject.replace('{group_id}', group_id);
        create<Group>(endpoint, group_data, group, Group.fromJSON, toast);
    }

    async function deleteGroup(id: string) {
        const endpoint = endpoints.groups.retrieve.replace('{id}', id);
        delete_id<Group>(endpoint, group, Group.fromJSON, toast);
    }

    return {
        groups,
        group,
        getGroupByID,
        getGroupsByProject,

        createGroup,
        deleteGroup
    };
}
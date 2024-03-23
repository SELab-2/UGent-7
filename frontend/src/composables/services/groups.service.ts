import {Group} from '@/types/Group.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList } from '@/composables/services/helpers.ts';

export function useGroup() {
    const groups = ref<Group[]|null>(null);
    const group = ref<Group|null>(null);

    async function getGroupByID(id: number) {
        const endpoint = endpoints.groups.retrieve.replace('{id}', id.toString());
        get<Group>(endpoint, group, Group.fromJSON);
        console.log(group)
    }

    async function getGroupsByProject(project_id: number) {
        const endpoint = endpoints.groups.byProject.replace('{project_id}', project_id.toString());
        getList<Group>(endpoint, groups, Group.fromJSON);
        console.log(groups.value ? groups.value.map((group, index) => `Group ${index + 1}: ${JSON.stringify(group)}`) : 'Groups is null');
    }

    return {
        groups,
        group,
        getGroupByID,
        getGroupsByProject
    };
}
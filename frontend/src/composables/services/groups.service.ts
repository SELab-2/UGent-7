import {Group} from '@/types/Group.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';
import {ComposerTranslation} from "vue-i18n";

export function useGroup() {
    const groups = ref<Group[]|null>(null);
    const group = ref<Group|null>(null);

    async function getGroupByID(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.groups.retrieve.replace('{id}', id);
        await get<Group>(endpoint, group, Group.fromJSON, t);
    }

    async function getGroupsByProject(project_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.groups.byProject.replace('{project_id}', project_id);
        await getList<Group>(endpoint, groups, Group.fromJSON, t);
    }

    async function createGroup(group_data: any, group_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.groups.byProject.replace('{group_id}', group_id);
        await create<Group>(endpoint, group_data, group, Group.fromJSON, t);
    }

    async function deleteGroup(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.groups.retrieve.replace('{id}', id);
        await delete_id<Group>(endpoint, group, Group.fromJSON, t);
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
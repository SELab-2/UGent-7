import {Group} from '@/types/Group.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';
import {ComposerTranslation} from "vue-i18n";

export function useGroup() {
    const groups = ref<Group[]|null>(null);
    const group = ref<Group|null>(null);
    const toast = useToast();

    async function getGroupByID(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.groups.retrieve.replace('{id}', id);
        await get<Group>(endpoint, group, Group.fromJSONFullObject, toast, t);
    }

    async function getGroupsByProject(project_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.groups.byProject.replace('{project_id}', project_id);
        await getList<Group>(endpoint, groups, Group.fromJSON, toast, t);
    }

    async function getGroupsByStudent(student_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.groups.byStudent.replace('{student_id}', student_id);
        await getList<Group>(endpoint, groups, Group.fromJSON, toast, t);
    }

    async function createGroup(group_data: any, group_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.groups.byProject.replace('{group_id}', group_id);
        create<Group>(endpoint, group_data, group, Group.fromJSON, toast, t);
    }

    async function deleteGroup(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.groups.retrieve.replace('{id}', id);
        delete_id<Group>(endpoint, group, Group.fromJSON, toast, t);
    }

    return {
        groups,
        group,
        getGroupByID,
        getGroupsByProject,
        getGroupsByStudent,

        createGroup,
        deleteGroup
    };
}
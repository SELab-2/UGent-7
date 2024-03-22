import {Group} from '@/types/Group.ts';
import {ref} from 'vue';
import axios from 'axios';
import {endpoints} from '@/config/endpoints.ts';

export function useGroup() {
    const groups = ref<Group[]|null>(null);
    const group = ref<Group|null>(null);

    async function getGroupByID(id: number) {
        const endpoint = endpoints.groups.retrieve.replace('{id}', id.toString());

        axios.get(endpoint).then(response => {
            group.value = Group.fromJSON(response.data);
        }).catch(error => {
            console.log(error.data);
        });

        console.log(group)
    }

    async function getGroupsByProject(project_id: number) {
        const endpoint = endpoints.groups.byProject.replace('{project_id}', project_id.toString());

        axios.get(endpoint).then(response => {
            groups.value = response.data.map((groupData: Group) => Group.fromJSON(groupData));
        }).catch(error => {
            console.log(error.data);
        });

        console.log(groups.value ? groups.value.map((group, index) => `Group ${index + 1}: ${JSON.stringify(group)}`) : 'Groups is null');
    }

    return {
        groups,
        group,
        getGroupByID,
        getGroupsByProject
    };
}
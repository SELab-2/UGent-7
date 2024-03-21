import {Admin} from '@/types/Admin.ts';
import {ref} from 'vue';
import axios from 'axios';
import {endpoints} from '@/config/endpoints.ts';

export function useAdmin() {
    const admins = ref<Admin[]|null>(null);
    const admin = ref<Admin|null>(null);

    async function getAdminByID(id: number) {
        const endpoint = endpoints.admins.retrieve.replace('{id}', id.toString());

        axios.get(endpoint).then(response => {
            admin.value = Admin.fromJSON(response.data);
        }).catch(error => {
            console.log(error.data);
        });

        console.log(admin)
    }

    return {
        admins,
        admin,
        getAdminByID
    };
}
import {Admin} from '@/types/Admin.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';

export function useAdmin() {
    const admins = ref<Admin[]|null>(null);
    const admin = ref<Admin|null>(null);

    async function getAdminByID(id: string) {
        const endpoint = endpoints.admins.retrieve.replace('{id}', id);
        await get<Admin>(endpoint, admin, Admin.fromJSON);
    }

    async function getAdmins() {
        const endpoint = endpoints.admins.index;
        await getList<Admin>(endpoint, admins, Admin.fromJSON);
    }

    async function createAdmin(admin_data: any) {
        const endpoint = endpoints.admins.index;
        await create<Admin>(endpoint, admin_data, admin, Admin.fromJSON);
    }

    async function deleteAdmin(id: string) {
        const endpoint = endpoints.admins.retrieve.replace('{id}', id);
        await delete_id<Admin>(endpoint, admin, Admin.fromJSON);
    }

    return {
        admins,
        admin,
        getAdminByID,
        getAdmins,

        createAdmin,
        deleteAdmin
    };
}
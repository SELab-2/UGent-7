import {Admin} from '@/types/Admin.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';

export function useAdmin() {
    const admins = ref<Admin[]|null>(null);
    const admin = ref<Admin|null>(null);
    const toast = useToast();

    async function getAdminByID(id: string) {
        const endpoint = endpoints.admins.retrieve.replace('{id}', id);
        get<Admin>(endpoint, admin, Admin.fromJSON, toast);
    }

    async function getAdmins() {
        const endpoint = endpoints.admins.index;
        getList<Admin>(endpoint, admins, Admin.fromJSON, toast);
    }


    async function createAdmin(admin_data: any) {
        const endpoint = endpoints.admins.index;
        create<Admin>(endpoint, admin_data, admin, Admin.fromJSON, toast);
    }

    async function deleteAdmin(id: string) {
        const endpoint = endpoints.admins.retrieve.replace('{id}', id.toString());
        delete_id<Admin>(endpoint, admin, Admin.fromJSON, toast);
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
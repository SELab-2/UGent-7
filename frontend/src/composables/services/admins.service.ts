import {Admin} from '@/types/Admin.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';

export function useAdmin() {
    const admins = ref<Admin[]|null>(null);
    const admin = ref<Admin|null>(null);
    const toast = useToast();

    async function getAdminByID(id: number) {
        const endpoint = endpoints.admins.retrieve.replace('{id}', id.toString());
        get<Admin>(endpoint, admin, Admin.fromJSON, toast);
        console.log(admin)
    }

    async function getAdmins() {
        const endpoint = endpoints.admins.index;
        getList<Admin>(endpoint, admins, Admin.fromJSON, toast);
        console.log(admins.value ? admins.value.map((admin, index) => `Admin ${index + 1}: ${JSON.stringify(admin)}`) : 'Admins is null');
    }

    return {
        admins,
        admin,
        getAdminByID,
        getAdmins
    };
}
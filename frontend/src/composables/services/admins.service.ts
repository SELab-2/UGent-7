import {Admin} from '@/types/Admin.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';
import {ComposerTranslation} from "vue-i18n";

export function useAdmin() {
    const admins = ref<Admin[]|null>(null);
    const admin = ref<Admin|null>(null);
    const toast = useToast();

    async function getAdminByID(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.admins.retrieve.replace('{id}', id);
        get<Admin>(endpoint, admin, Admin.fromJSON, toast, t);
    }

    async function getAdmins(t: ComposerTranslation) {
        const endpoint = endpoints.admins.index;
        getList<Admin>(endpoint, admins, Admin.fromJSON, toast, t);
    }

    async function createAdmin(admin_data: any, t: ComposerTranslation) {
        const endpoint = endpoints.admins.index;
        create<Admin>(endpoint, admin_data, admin, Admin.fromJSON, toast, t);
    }

    async function deleteAdmin(id: string, , t: ComposerTranslation) {
        const endpoint = endpoints.admins.retrieve.replace('{id}', id);
        delete_id<Admin>(endpoint, admin, Admin.fromJSON, toast, t);
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
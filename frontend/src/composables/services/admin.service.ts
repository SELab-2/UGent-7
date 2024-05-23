import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList, deleteId, createToast } from '@/composables/services/helpers.ts';
import { User } from '@/types/users/User.ts';

interface AdminState {
    admins: Ref<User[] | null>;
    admin: Ref<User | null>;
    getAdminByID: (id: string, selfProcessError?: boolean) => Promise<void>;
    getAdmins: (selfProcessError?: boolean) => Promise<void>;
    createAdmin: (adminData: User, selfProcessError?: boolean) => Promise<void>;
    deleteAdmin: (id: string, selfProcessError?: boolean) => Promise<void>;
}

export function useAdmin(): AdminState {
    const admins = ref<User[] | null>(null);
    const admin = ref<User | null>(null);

    async function getAdminByID(id: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.admins.retrieve.replace('{id}', id);
        await get<User>(endpoint, admin, User.fromJSON, selfProcessError);
    }

    async function getAdmins(selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.admins.index;
        await getList<User>(endpoint, admins, User.fromJSON, selfProcessError);
    }

    async function createAdmin(user: User, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.admins.index;
        await createToast<User>(
            'admin',
            endpoint,
            {
                id: user.id,
            },
            admin,
            User.fromJSON,
            undefined,
            selfProcessError,
        );
    }

    async function deleteAdmin(id: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.admins.retrieve.replace('{id}', id);
        await deleteId<User>(endpoint, admin, User.fromJSON, selfProcessError);
    }

    return {
        admins,
        admin,

        getAdminByID,
        getAdmins,

        createAdmin,
        deleteAdmin,
    };
}

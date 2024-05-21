import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList, create, deleteId } from '@/composables/services/helpers.ts';
import { User } from '@/types/users/User.ts';

interface AdminState {
    admins: Ref<User[] | null>;
    admin: Ref<User | null>;
    getAdminByID: (id: string, selfprocessError?: boolean) => Promise<void>;
    getAdmins: (selfprocessError?: boolean) => Promise<void>;
    createAdmin: (adminData: User, selfprocessError?: boolean) => Promise<void>;
    deleteAdmin: (id: string, selfprocessError?: boolean) => Promise<void>;
}

export function useAdmin(): AdminState {
    const admins = ref<User[] | null>(null);
    const admin = ref<User | null>(null);

    async function getAdminByID(id: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.admins.retrieve.replace('{id}', id);
        await get<User>(endpoint, admin, User.fromJSON, selfprocessError);
    }

    async function getAdmins(selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.admins.index;
        await getList<User>(endpoint, admins, User.fromJSON, selfprocessError);
    }

    async function createAdmin(user: User, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.admins.index;
        await create<User>(
            endpoint,
            {
                id: user.id,
            },
            admin,
            User.fromJSON,
            undefined,
            selfprocessError
        );
    }

    async function deleteAdmin(id: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.admins.retrieve.replace('{id}', id);
        await deleteId<User>(endpoint, admin, User.fromJSON, selfprocessError);
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

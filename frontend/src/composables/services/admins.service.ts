import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList, create, deleteId } from '@/composables/services/helpers.ts';
import { User } from '@/types/users/User.ts';

interface AdminState {
    admins: Ref<User[] | null>;
    admin: Ref<User | null>;
    getAdminByID: (id: string) => Promise<void>;
    getAdmins: () => Promise<void>;
    createAdmin: (adminData: User) => Promise<void>;
    deleteAdmin: (id: string) => Promise<void>;
}

export function useAdmin(): AdminState {
    const admins = ref<User[] | null>(null);
    const admin = ref<User | null>(null);

    async function getAdminByID(id: string): Promise<void> {
        const endpoint = endpoints.admins.retrieve.replace('{id}', id);
        await get<User>(endpoint, admin, User.fromJSON);
    }

    async function getAdmins(): Promise<void> {
        const endpoint = endpoints.admins.index;
        await getList<User>(endpoint, admins, User.fromJSON);
    }

    async function createAdmin(adminData: User): Promise<void> {
        const endpoint = endpoints.admins.index;
        await create<User>(
            endpoint,
            {
                email: adminData.email,
                first_name: adminData.first_name,
                last_name: adminData.last_name,
            },
            admin,
            User.fromJSON,
        );
    }

    async function deleteAdmin(id: string): Promise<void> {
        const endpoint = endpoints.admins.retrieve.replace('{id}', id);
        await deleteId<User>(endpoint, admin, User.fromJSON);
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

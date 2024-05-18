import { type Ref, ref } from 'vue';
import { User } from '@/types/users/User.ts';
import { type Response } from '@/types/Response.ts';
import { type PaginatorResponse } from '@/types/filter/Paginator.ts';
import { endpoints } from '@/config/endpoints.ts';
import { get, patch, getList, getPaginatedList, createToast } from '@/composables/services/helpers.ts';
import { type Filter } from '@/types/filter/Filter.ts';

interface userState {
    pagination: Ref<PaginatorResponse<User> | null>;
    users: Ref<User[] | null>;
    user: Ref<User | null>;
    getUserByID: (id: string) => Promise<void>;
    getUsers: () => Promise<void>;
    searchUsers: (filters: Filter, page: number, pageSize: number) => Promise<void>;
    createUser: (user_data: User) => Promise<void>;
    toggleAdmin: (id: string, is_staff: boolean) => Promise<void>;
}

export function useUser(): userState {
    const pagination = ref<PaginatorResponse<User> | null>(null);
    const users = ref<User[] | null>(null);
    const user = ref<User | null>(null);
    const response = ref<Response | null>(null);

    async function getUserByID(id: string): Promise<void> {
        const endpoint = endpoints.users.retrieve.replace('{id}', id);
        await get<User>(endpoint, user, User.fromJSON);
    }

    async function getUsers(): Promise<void> {
        const endpoint = endpoints.users.index;
        await getList<User>(endpoint, users, User.fromJSON);
    }

    async function searchUsers(filters: Filter, page: number, pageSize: number): Promise<void> {
        const endpoint = endpoints.users.search;
        await getPaginatedList<User>(endpoint, filters, page, pageSize, pagination, User.fromJSON);
    }

    async function createUser(userData: User): Promise<void> {
        const endpoint = endpoints.users.index;
        await createToast<User>(
            'user',
            endpoint,
            {
                username: userData.username,
                is_staff: userData.is_staff,
                email: userData.email,
                first_name: userData.first_name,
                last_name: userData.last_name,
            },
            user,
            User.fromJSON,
        );
    }

    async function toggleAdmin(id: string, isStaff: boolean): Promise<void> {
        const endpoint = endpoints.users.admin.replace('{id}', id);
        await patch(
            endpoint,
            {
                is_staff: isStaff,
            },
            response,
        );
    }

    return {
        pagination,
        users,
        user,

        getUserByID,
        getUsers,
        searchUsers,
        createUser,
        toggleAdmin,
    };
}

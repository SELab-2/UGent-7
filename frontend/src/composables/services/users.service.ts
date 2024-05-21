import { type Ref, ref } from 'vue';
import { User } from '@/types/users/User.ts';
import { type Response } from '@/types/Response.ts';
import { type PaginatorResponse } from '@/types/filter/Paginator.ts';
import { endpoints } from '@/config/endpoints.ts';
import { create, get, patch, getList, getPaginatedList } from '@/composables/services/helpers.ts';
import { type Filter } from '@/types/filter/Filter.ts';

interface userState {
    pagination: Ref<PaginatorResponse<User> | null>;
    users: Ref<User[] | null>;
    user: Ref<User | null>;
    getUserByID: (id: string, selfprocessError?: boolean) => Promise<void>;
    getUsers: (selfprocessError?: boolean) => Promise<void>;
    searchUsers: (filters: Filter, page: number, pageSize: number, selfprocessError?: boolean) => Promise<void>;
    createUser: (user_data: User, selfprocessError?: boolean) => Promise<void>;
    toggleAdmin: (id: string, is_staff: boolean, selfprocessError?: boolean) => Promise<void>;
}

export function useUser(): userState {
    const pagination = ref<PaginatorResponse<User> | null>(null);
    const users = ref<User[] | null>(null);
    const user = ref<User | null>(null);
    const response = ref<Response | null>(null);

    async function getUserByID(id: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.users.retrieve.replace('{id}', id);
        await get<User>(endpoint, user, User.fromJSON, selfprocessError);
    }

    async function getUsers(selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.users.index;
        await getList<User>(endpoint, users, User.fromJSON, selfprocessError);
    }

    async function searchUsers(
        filters: Filter,
        page: number,
        pageSize: number,
        selfprocessError: boolean = true
    ): Promise<void> {
        const endpoint = endpoints.users.search;
        await getPaginatedList<User>(endpoint, filters, page, pageSize, pagination, User.fromJSON, selfprocessError);
    }

    async function createUser(userData: User, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.users.index;
        await create<User>(
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
            undefined,
            selfprocessError,
        );
    }

    async function toggleAdmin(id: string, isStaff: boolean, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.users.admin.replace('{id}', id);
        await patch(
            endpoint,
            {
                is_staff: isStaff,
            },
            response,
            undefined,
            selfprocessError,
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

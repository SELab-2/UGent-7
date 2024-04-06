import {ref} from "vue";
import {User} from "@/types/users/User.ts";
import {PaginatorResponse} from "@/types/filter/Paginator.ts";
import {endpoints} from "@/config/endpoints.ts";
import {create, get, getList, getPaginatedList} from "@/composables/services/helpers.ts";
import {Filter} from "@/types/filter/Filter.ts";


export function useUser() {
    const pagination = ref<PaginatorResponse<User> | null>(null);
    const users = ref<User[]|null>(null);
    const user = ref<User|null>(null);

    async function getUserByID(id: string) {
        const endpoint = endpoints.users.retrieve.replace('{id}', id);
        await get<User>(endpoint, user, User.fromJSON);
    }

    async function getUsers() {
        const endpoint = endpoints.users.index;
        await getList<User>(endpoint, users, User.fromJSON);
    }

    async function searchUsers(filters: Filter, page: number, pageSize: number) {
        const endpoint = endpoints.users.search;
        await getPaginatedList<User>(endpoint, filters, page, pageSize, pagination, User.fromJSON);
    }

    async function createUser(user_data: User) {
        const endpoint = endpoints.users.index
        await create<User>(endpoint,
            {
                username: user_data.username,
                is_staff: user_data.is_staff,
                email: user_data.email,
                first_name: user_data.first_name,
                last_name: user_data.last_name
            },
            user, User.fromJSON)
    }

    return {
        pagination,
        users,
        user,

        getUserByID,
        getUsers,
        searchUsers,
        createUser
    }
}
import {ref} from "vue";
import {User} from "@/types/User.ts";
import {endpoints} from "@/config/endpoints.ts";
import {create, get, getList} from "@/composables/services/helpers.ts";


export function useUser() {
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
        users,
        user,

        getUserByID,
        getUsers,
        createUser
    }
}
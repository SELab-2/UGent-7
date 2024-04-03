import {ref} from "vue";
import {User} from "@/types/User.ts";
import {endpoints} from "@/config/endpoints.ts";
import {get, getList} from "@/composables/services/helpers.ts";


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

    return {
        users,
        user,

        getUserByID,
        getUsers
    }
}
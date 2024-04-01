import { ref } from 'vue'
import { endpoints } from '@/config/endpoints.ts'
import {
    get,
    getList,
    create,
    deleteId
} from '@/composables/services/helpers.ts'
import { User } from '@/types/User.ts'

export function useAdmin() {
    const admins = ref<User[] | null>(null)
    const admin = ref<User | null>(null)

    async function getAdminByID(id: string) {
        const endpoint = endpoints.admins.retrieve.replace('{id}', id)
        await get<User>(endpoint, admin, User.fromJSON)
    }

    async function getAdmins() {
        const endpoint = endpoints.admins.index
        await getList<User>(endpoint, admins, User.fromJSON)
    }

    async function createAdmin(adminData: User) {
        const endpoint = endpoints.admins.index
        await create<User>(
            endpoint,
            {
                email: adminData.email,
                first_name: adminData.first_name,
                last_name: adminData.last_name
            },
            admin,
            User.fromJSON
        )
    }

    async function deleteAdmin(id: string) {
        const endpoint = endpoints.admins.retrieve.replace('{id}', id)
        await deleteId<User>(endpoint, admin, User.fromJSON)
    }

    return {
        admins,
        admin,
        getAdminByID,
        getAdmins,

        createAdmin,
        deleteAdmin
    }
}

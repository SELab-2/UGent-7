import { Faculty } from '@/types/Faculty.ts'
import { ref } from 'vue'
import { endpoints } from '@/config/endpoints.ts'
import {
    get,
    getList,
    create,
    delete_id
} from '@/composables/services/helpers.ts'

export function useFaculty() {
    const faculties = ref<Faculty[] | null>(null)
    const faculty = ref<Faculty | null>(null)

    async function getFacultyByID(name: string) {
        const endpoint = endpoints.faculties.retrieve.replace('{name}', name)
        await get<Faculty>(endpoint, faculty, Faculty.fromJSON)
    }

    async function getFacultys() {
        const endpoint = endpoints.faculties.index
        await getList<Faculty>(endpoint, faculties, Faculty.fromJSON)
    }

    async function createFaculty(faculty_data: Faculty) {
        const endpoint = endpoints.faculties.index
        await create<Faculty>(
            endpoint,
            { name: faculty_data.name },
            faculty,
            Faculty.fromJSON
        )
    }

    async function deleteFaculty(id: string) {
        const endpoint = endpoints.faculties.retrieve.replace('{id}', id)
        await delete_id<Faculty>(endpoint, faculty, Faculty.fromJSON)
    }

    return {
        faculties,
        faculty,
        getFacultyByID,
        getFacultys,

        createFaculty,
        deleteFaculty
    }
}

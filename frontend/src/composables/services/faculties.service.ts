import {Faculty} from '@/types/Faculty.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';
import {ComposerTranslation} from "vue-i18n";

export function useFaculty() {
    const faculties = ref<Faculty[]|null>(null);
    const faculty = ref<Faculty|null>(null);

    async function getFacultyByID(name: string, t: ComposerTranslation) {
        const endpoint = endpoints.faculties.retrieve.replace('{name}', name);
        await get<Faculty>(endpoint, faculty, Faculty.fromJSON, t);
    }

    async function getFacultys(t: ComposerTranslation) {
        const endpoint = endpoints.faculties.index;
        await getList<Faculty>(endpoint, faculties, Faculty.fromJSON, t);
    }

    async function createFaculty(faculty_data: any, t: ComposerTranslation) {
        const endpoint = endpoints.faculties.index;
        await create<Faculty>(endpoint, faculty_data, faculty, Faculty.fromJSON, t);
    }

    async function deleteFaculty(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.faculties.retrieve.replace('{id}', id);
        await delete_id<Faculty>(endpoint, faculty, Faculty.fromJSON, t);
    }

    return {
        faculties,
        faculty,
        getFacultyByID,
        getFacultys,

        createFaculty,
        deleteFaculty
    };
}
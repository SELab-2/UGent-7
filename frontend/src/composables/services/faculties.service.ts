import {Faculty} from '@/types/Faculty.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';
import {ComposerTranslation} from "vue-i18n";

export function useFaculty() {
    const faculties = ref<Faculty[]|null>(null);
    const faculty = ref<Faculty|null>(null);
    const toast = useToast();

    async function getFacultyByID(name: string, t: ComposerTranslation) {
        const endpoint = endpoints.faculties.retrieve.replace('{name}', name);
        get<Faculty>(endpoint, faculty, Faculty.fromJSON, toast, t);
    }

    async function getFacultys(t: ComposerTranslation) {
        const endpoint = endpoints.faculties.index;
        getList<Faculty>(endpoint, faculties, Faculty.fromJSON, toast, t);
    }

    async function createFaculty(faculty_data: any, t: ComposerTranslation) {
        const endpoint = endpoints.faculties.index;
        create<Faculty>(endpoint, faculty_data, faculty, Faculty.fromJSON, toast, t);
    }

    async function deleteFaculty(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.faculties.retrieve.replace('{id}', id);
        delete_id<Faculty>(endpoint, faculty, Faculty.fromJSON, toast, t);
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
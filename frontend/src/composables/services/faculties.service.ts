import {Faculty} from '@/types/Faculty.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';

export function useFaculty() {
    const faculties = ref<Faculty[]|null>(null);
    const faculty = ref<Faculty|null>(null);
    const toast = useToast();

    async function getFacultyByID(name: string) {
        const endpoint = endpoints.faculties.retrieve.replace('{name}', name);
        get<Faculty>(endpoint, faculty, Faculty.fromJSON, toast);
    }

    async function getFacultys() {
        const endpoint = endpoints.faculties.index;
        getList<Faculty>(endpoint, faculties, Faculty.fromJSON, toast);
    }

    async function createFaculty(faculty_data: any) {
        const endpoint = endpoints.faculties.index;
        create<Faculty>(endpoint, faculty_data, faculty, Faculty.fromJSON, toast);
    }

    async function deleteFaculty(id: string) {
        const endpoint = endpoints.faculties.retrieve.replace('{id}', id);
        delete_id<Faculty>(endpoint, faculty, Faculty.fromJSON, toast);
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
import {Faculty} from '@/types/Faculty.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';

export function useFaculty() {
    const faculties = ref<Faculty[]|null>(null);
    const faculty = ref<Faculty|null>(null);
    const toast = useToast();

    async function getFacultyByID(name: string) {
        const endpoint = endpoints.faculties.retrieve.replace('{name}', name);
        get<Faculty>(endpoint, faculty, Faculty.fromJSON, toast);
        console.log(faculty)
    }

    async function getFacultys() {
        const endpoint = endpoints.faculties.index;
        getList<Faculty>(endpoint, faculties, Faculty.fromJSON, toast);
        console.log(faculties.value ? faculties.value.map((faculty, index) => `Faculty ${index + 1}: ${JSON.stringify(faculty)}`) : 'Facultys is null');
    }

    return {
        faculties,
        faculty,
        getFacultyByID,
        getFacultys
    };
}
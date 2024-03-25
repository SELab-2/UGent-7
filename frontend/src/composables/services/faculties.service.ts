import {Faculty} from '@/types/Faculty.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';
import {ComposerTranslation} from "vue-i18n";

export function useFaculty() {
    const faculties = ref<Faculty[]|null>(null);
    const faculty = ref<Faculty|null>(null);
    const toast = useToast();

    async function getFacultyByID(name: string, t: ComposerTranslation) {
        const endpoint = endpoints.faculties.retrieve.replace('{name}', name);
        get<Faculty>(endpoint, faculty, Faculty.fromJSON, toast, t);
        console.log(faculty)
    }

    async function getFacultys(t: ComposerTranslation) {
        const endpoint = endpoints.faculties.index;
        getList<Faculty>(endpoint, faculties, Faculty.fromJSON, toast, t);
        console.log(faculties.value ? faculties.value.map((faculty, index) => `Faculty ${index + 1}: ${JSON.stringify(faculty)}`) : 'Facultys is null');
    }

    return {
        faculties,
        faculty,
        getFacultyByID,
        getFacultys
    };
}
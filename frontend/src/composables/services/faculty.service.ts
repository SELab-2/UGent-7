import { Faculty } from '@/types/Faculty.ts';
import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList, deleteId, create } from '@/composables/services/helpers.ts';

interface FacultyState {
    faculties: Ref<Faculty[] | null>;
    faculty: Ref<Faculty | null>;
    getFacultyByID: (id: string, selfProcessError?: boolean) => Promise<void>;
    getFaculties: (selfProcessError?: boolean) => Promise<void>;
    createFaculty: (facultyData: Faculty, selfProcessError?: boolean) => Promise<void>;
    deleteFaculty: (id: string, selfProcessError?: boolean) => Promise<void>;
}

export function useFaculty(): FacultyState {
    const faculties = ref<Faculty[] | null>(null);
    const faculty = ref<Faculty | null>(null);

    async function getFacultyByID(id: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.faculties.retrieve.replace('{id}', id);
        await get<Faculty>(endpoint, faculty, Faculty.fromJSON, selfProcessError);
    }

    async function getFaculties(selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.faculties.index;
        await getList<Faculty>(endpoint, faculties, Faculty.fromJSON, selfProcessError);
    }

    async function createFaculty(facultyData: Faculty, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.faculties.index;
        await create<Faculty>(
            endpoint,
            { id: facultyData.id, name: facultyData.name },
            faculty,
            Faculty.fromJSON,
            undefined,
            selfProcessError,
        );
    }

    async function deleteFaculty(id: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.faculties.retrieve.replace('{id}', id);
        await deleteId<Faculty>(endpoint, faculty, Faculty.fromJSON, selfProcessError);
    }

    return {
        faculties,
        faculty,
        getFacultyByID,
        getFaculties,

        createFaculty,
        deleteFaculty,
    };
}

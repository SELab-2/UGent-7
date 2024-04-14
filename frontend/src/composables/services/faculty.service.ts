import { Faculty } from '@/types/Faculty.ts';
import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList, create, deleteId } from '@/composables/services/helpers.ts';

interface FacultyState {
    faculties: Ref<Faculty[] | null>;
    faculty: Ref<Faculty | null>;
    getFacultyByID: (id: string) => Promise<void>;
    getFaculties: () => Promise<void>;
    createFaculty: (facultyData: Faculty) => Promise<void>;
    deleteFaculty: (id: string) => Promise<void>;
}

export function useFaculty(): FacultyState {
    const faculties = ref<Faculty[] | null>(null);
    const faculty = ref<Faculty | null>(null);

    async function getFacultyByID(id: string): Promise<void> {
        const endpoint = endpoints.faculties.retrieve.replace('{id}', id);
        await get<Faculty>(endpoint, faculty, Faculty.fromJSON);
    }

    async function getFaculties(): Promise<void> {
        const endpoint = endpoints.faculties.index;
        await getList<Faculty>(endpoint, faculties, Faculty.fromJSON);
    }

    async function createFaculty(facultyData: Faculty): Promise<void> {
        const endpoint = endpoints.faculties.index;
        await create<Faculty>(endpoint, { id: facultyData.id, name: facultyData.name }, faculty, Faculty.fromJSON);
    }

    async function deleteFaculty(id: string): Promise<void> {
        const endpoint = endpoints.faculties.retrieve.replace('{id}', id);
        await deleteId<Faculty>(endpoint, faculty, Faculty.fromJSON);
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
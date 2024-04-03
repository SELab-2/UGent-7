import { Faculty } from '@/types/Faculty.ts';
import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList, create, deleteId } from '@/composables/services/helpers.ts';

interface FacultyState {
    faculties: Ref<Faculty[] | null>;
    faculty: Ref<Faculty | null>;
    getFacultyByID: (name: string) => Promise<void>;
    getFacultys: () => Promise<void>;
    createFaculty: (facultyData: Faculty) => Promise<void>;
    deleteFaculty: (id: string) => Promise<void>;
}

export function useFaculty(): FacultyState {
    const faculties = ref<Faculty[] | null>(null);
    const faculty = ref<Faculty | null>(null);

    async function getFacultyByID(name: string): Promise<void> {
        const endpoint = endpoints.faculties.retrieve.replace('{name}', name);
        await get<Faculty>(endpoint, faculty, Faculty.fromJSON);
    }

    async function getFacultys(): Promise<void> {
        const endpoint = endpoints.faculties.index;
        await getList<Faculty>(endpoint, faculties, Faculty.fromJSON);
    }

    async function createFaculty(facultyData: Faculty): Promise<void> {
        const endpoint = endpoints.faculties.index;
        await create<Faculty>(endpoint, { name: facultyData.name }, faculty, Faculty.fromJSON);
    }

    async function deleteFaculty(id: string): Promise<void> {
        const endpoint = endpoints.faculties.retrieve.replace('{id}', id);
        await deleteId<Faculty>(endpoint, faculty, Faculty.fromJSON);
    }

    return {
        faculties,
        faculty,
        getFacultyByID,
        getFacultys,

        createFaculty,
        deleteFaculty,
    };
}

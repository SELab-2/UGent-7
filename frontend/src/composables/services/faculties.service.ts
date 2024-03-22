import {Faculty} from '@/types/Faculty.ts';
import {ref} from 'vue';
import axios from 'axios';
import {endpoints} from '@/config/endpoints.ts';

export function useFaculty() {
    const faculties = ref<Faculty[]|null>(null);
    const faculty = ref<Faculty|null>(null);

    async function getFacultyByID(name: string) {
        const endpoint = endpoints.faculties.retrieve.replace('{name}', name);

        axios.get(endpoint).then(response => {
            faculty.value = Faculty.fromJSON(response.data);
        }).catch(error => {
            console.log(error.data);
        });

        console.log(faculty)
    }

    return {
        faculties,
        faculty,
        getFacultyByID
    };
}
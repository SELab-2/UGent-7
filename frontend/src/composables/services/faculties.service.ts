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

    async function getFacultys() {
        const endpoint = endpoints.faculties.index;

        axios.get(endpoint).then(response => {
            faculties.value = response.data.map((facultyData: Faculty) => Faculty.fromJSON(facultyData));
        }).catch(error => {
            console.log(error.data);
        });

        console.log(faculties.value ? faculties.value.map((faculty, index) => `Faculty ${index + 1}: ${JSON.stringify(faculty)}`) : 'Facultys is null');
    }

    return {
        faculties,
        faculty,
        getFacultyByID,
        getFacultys
    };
}
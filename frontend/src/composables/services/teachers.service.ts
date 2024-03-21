import {Teacher} from '@/types/Teacher.ts';
import {ref} from 'vue';
import axios from 'axios';
import {endpoints} from '@/config/endpoints.ts';

export function useTeacher() {
    const teachers = ref<Teacher[]|null>(null);
    const teacher = ref<Teacher|null>(null);

    async function getTeacherByID(id: number) {
        const endpoint = endpoints.teachers.retrieve.replace('{id}', id.toString());

        axios.get(endpoint).then(response => {
            teacher.value = Teacher.fromJSON(response.data);
        }).catch(error => {
            console.log(error.data);
        });

        console.log(teacher)
    }

    return {
        teachers,
        teacher,
        getTeacherByID
    };
}
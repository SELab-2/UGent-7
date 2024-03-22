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

    async function getTeachers() {
        const endpoint = endpoints.teachers.index;

        axios.get(endpoint).then(response => {
            teachers.value = response.data.map((teacherData: Teacher) => Teacher.fromJSON(teacherData));
        }).catch(error => {
            console.log(error.data);
        });

        console.log(teachers.value ? teachers.value.map((teacher, index) => `Teacher ${index + 1}: ${JSON.stringify(teacher)}`) : 'Teachers is null');
    }

    return {
        teachers,
        teacher,
        getTeacherByID,
        getTeachers
    };
}